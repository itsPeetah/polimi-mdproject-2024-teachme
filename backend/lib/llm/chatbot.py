"""Chatbots for TeachMe project.
"""

import warnings
import time

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

from .PROMPTS import get_prompt
from ..database import Connector, MongoDBConnector, MongoDB, Conversation
from ..log import LogType, Log, Logger


class BaseChatBot:
    """
    Base class for chatbot implementations.

    :ivar str api_key: API key for accessing the chatbot model.
    :ivar float temperature: Sampling temperature parameter for generating responses.
    :ivar BaseChatModel _chat_base: Instance of the chat model used by the bot.
    """

    def __init__(
        self,
        api_key: str,
        model: BaseChatModel = ChatOpenAI,
        model_version: str = "gpt-3.5-turbo",
        temperature: float = 0.2,
        logger: Logger = None,
    ):
        self.api_key = api_key
        self.temperature = temperature
        self.logger = logger

        self._chat_base = model(
            model=model_version,
            api_key=self.api_key,
            temperature=temperature,
        )

    def log(self, message: str):
        """Logs a message using the logger if available, otherwise prints it to the console.

        :param message: The message to log.
        :type message: str
        """
        if self.logger is not None:
            self.logger.log(Log(LogType.CHATBOT, message))
        else:
            print(f"CHATBOT - {message}")


class ConversationalChatBot(BaseChatBot):
    def __init__(
        self,
        api_key: str,
        conversation_id: str,
        model: BaseChatModel = ChatOpenAI,
        model_version: str = "gpt-3.5-turbo",
        temperature: float = 0.2,
        db: MongoDB = None,
        idle_timeout: int = 300,  # in seconds | 300 seconds = 5 minutes
        logger: Logger = None,
    ):
        super().__init__(api_key, model, model_version, temperature, logger)

        self._db = db

        # Check if the data already exists in the database collection
        # named 'conversations'
        if db is not None:
            conversations = db.get_collection("conversations")
            conversation = conversations.find_by_id(conversation_id)
            if conversation is None:
                self.log(
                    f"""This error has been raised by the {self.__class__.__name__} class.
                         The conversation with ID {conversation_id} was not found in the database, meaning that it has not been created yet."""
                )

                raise ValueError(
                    "The conversation with the given ID was not found in the database."
                )

        self._conversation_id = conversation._id
        self._conversation_user_level = conversation.user_level
        self._conversation_difficulty = conversation.difficulty
        self._conversation_topic = conversation.topic

        # The chatbot should be active if the conversation is not ended yet.
        self._is_active = not conversation.is_ended

        # Attribute to check the timestamp of the last message sent by the user
        self._last_user_message_timestamp = time.time()
        self._idle_timeout = idle_timeout

        # Checking if the parameters have been set,
        # otherwise, if the conversation is not found in the database, raise an error
        # while if the others are not found, set them to default values.
        if self._conversation_id is None:
            raise ValueError("The conversation ID must be set.")

        if self._conversation_user_level is None:
            self._conversation_user_level = "intermediate"

        if self._conversation_difficulty is None:
            self._conversation_difficulty = "medium"

        if self._conversation_topic is None:
            self._conversation_topic = (
                "No specific topic has been set. The conversation is open to any topic."
            )
        else:
            self._conversation_topic = (
                f"The conversation topic is {self._conversation_topic}."
            )

        self._chat = None
        self._config = None

        self.load_chat_history()

    def _create_end_conversation_tool(self):
        @tool
        def end_conversation():
            """Greet the user and terminate the conversation."""

            self._is_active = False

            self.logger.log(
                Log(
                    LogType.CHATBOT,
                    f"The conversation with ID {self._conversation_id} has ended.",
                )
            )

        return end_conversation

    def load_chat_history(self):
        """
        Loads chat history and initializes chat configurations.

        This method constructs a chat prompt template based on the system prompt, conversation history, and user input.
        It then combines the prompt with the chat model to create a chat instance with history.
        Finally, it configures the chat session with the conversation ID.

        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"{get_prompt(prompt_name='CONVERSATIONAL_SYSTEM_PROMPT', user_level=self._conversation_user_level, conversation_difficulty=self._conversation_difficulty, conversation_topic=self._conversation_topic)}",
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{answer}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        tools = [self._create_end_conversation_tool()]
        agent = create_openai_tools_agent(self._chat_base, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

        self._chat = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: MongoDBChatMessageHistory(
                connection_string=self._db.db_connection_string,
                session_id=session_id,
                database_name=self._db.db_name,
                collection_name="chat_message_history",
            ),
            input_messages_key="answer",
            output_messages_key="output",
            history_messages_key="history",
        )
        self._config = {"configurable": {
            "session_id": f"{self._conversation_id}"}}

    def _get_message_history(self, session_id: int) -> str:
        if self._db is None:
            warnings.warn(
                "No database connection provided. Returning empty string.")
            return ""

        return (
            MongoDBChatMessageHistory(
                connection_string=self._db.db_connection_string,
                session_id=session_id,
                database_name=self._db.db_name,
                collection_name="chat_message_history",
            ),
        )

    def send_message(self, message: str) -> dict:
        """Sends a message to the chatbot and returns the response.

        :param message: The message to send by the user to the chatbot.
        :type message: str
        :return: The response from the chatbot. It includes the chatbot's output and the chatbot's active status.
        :rtype: dict
        """
        # Reset the timestamp of the last user message
        self._last_user_message_timestamp = time.time()

        if self._is_active is False:
            return {
                "output": "The chatbot is not active. The conversation has ended.",
                "is_chatbot_active": self._is_active,
            }

        # Invoke the chat model with the user message
        response = self._chat.invoke(
            {"answer": message},
            config=self._config,
        )

        chatbot_response = {
            "output": response.get("output"),
            "is_chatbot_active": self._is_active,
        }

        return chatbot_response

    def deactivate(self):
        """Deactivates the chatbot."""
        self._is_active = False

    @property
    def conversation_id(self) -> str:
        """Returns the conversation ID of the conversation the chatbot is assigned to.

        :return: The conversation ID.
        :rtype: str
        """
        return self._conversation_id

    @property
    def is_idle(self):
        """
        Returns True if the chatbot is idle, False otherwise.

        The idle state is determined by the time elapsed since the last user message.

        :return: True if the chatbot is idle, False otherwise.
        :rtype: bool
        """
        elapsed_time = time.time() - self._last_user_message_timestamp

        if elapsed_time > self._idle_timeout:
            self.logger.log(
                Log(
                    LogType.CHATBOT,
                    f"The conversation with ID {self._conversation_id} is idling. Elapsed time: {elapsed_time} seconds.",
                )
            )
            self._is_active = False
            result = True
        else:
            result = False

        return result


def test_chatbot(
    api_key: str,
    conversation_id: str,
    db: MongoDB,
    logger: Logger = None,
):
    """Helper method to test the conversational chatbot functionalities.

    :param api_key: chatbot provider API key
    :type api_key: str
    :param conversation_id: ID of the conversation
    :type conversation_id: str
    :param db: MongoDB database connection
    :type db: MongoDB
    :param logger: application logger, defaults to None
    :type logger: Logger, optional
    """
    chatbot = ConversationalChatBot(
        api_key=api_key,
        conversation_id=conversation_id,
        db=db,
        logger=logger,
    )
    while chatbot._is_active:
        bot_answer = chatbot.send_message(str(input("User message: ")))
        print(f"Bot answer: {bot_answer.get('output')}")
