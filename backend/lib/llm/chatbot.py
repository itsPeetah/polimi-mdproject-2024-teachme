"""Chatbots for TeachMe project.
"""

import warnings

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
# from langchain.chains import OpenAIModerationChain

from .PROMPTS import get_prompt
from ..database import Connector, MongoDBConnector, Conversation


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
    ):
        self.api_key = api_key
        self.temperature = temperature

        self._chat_base = model(
            model=model_version,
            api_key=self.api_key,
            temperature=temperature,
        )
        
        # self.content_mod_chain = OpenAIModerationChain()


class ConversationalChatBot(BaseChatBot):
    def __init__(
        self,
        api_key: str,
        conversation_id: int,
        conversation_user_level: str = None,
        conversation_difficulty: str = None,
        conversation_topic: str = None,
        model: BaseChatModel = ChatOpenAI,
        model_version: str = "gpt-3.5-turbo",
        temperature: float = 0.2,
        db_connector: Connector = None,
        db_name: str = "teachme_main",
    ):
        super().__init__(api_key, model, model_version, temperature)

        self._db_connector = db_connector
        self._db_name = db_name

        # Check if the data already exists in the database collection
        # named 'conversations'
        if self._db_connector is not None:
            db = self._db_connector.connect(self._db_name)
            conversations = db.get_collection("conversations")
            conversation = conversations.find_by_id(conversation_id)
            if conversation is None:
                conversation = Conversation(
                    _id = None,
                    conversation_id=conversation_id, 
                    user_level=conversation_user_level, 
                    difficulty=conversation_difficulty, 
                    topic=conversation_topic
                )
                conversations.insert_one(conversation_id = conversation.conversation_id, user_level = conversation.user_level, difficulty = conversation.difficulty, topic = conversation.topic)

            conversation_user_level = conversation.user_level
            conversation_difficulty = conversation.difficulty
            conversation_topic = conversation.topic

        self._conversation_id = conversation_id
        self._conversation_user_level = conversation_user_level
        self._conversation_difficulty = conversation_difficulty
        self._conversation_topic = conversation_topic

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
            self._conversation_topic = "No specific topic has been set, so the conversation is open to any topic."

        self._chat = None
        self._config = None

        self.load_chat_history()

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
            ]
        )

        _chat_with_history = prompt | self._chat_base # | self.content_mod_chain

        self._chat = RunnableWithMessageHistory(
            _chat_with_history,
            lambda session_id: MongoDBChatMessageHistory(
                connection_string=self._db_connector.connection_string,
                session_id=session_id,
                database_name=self._db_name,
                collection_name="chat_message_history",
            ),
            input_messages_key="answer",
            history_messages_key="history",
        )
        self._config = {"configurable": {"session_id": f"{self._conversation_id}"}}

    def _get_message_history(self, session_id: int) -> str:
        if self._db_connector is None:
            warnings.warn("No database connection provided. Returning empty string.")
            return ""

        return (
            MongoDBChatMessageHistory(
                connection_string=self._db_connector.connection_string,
                session_id=session_id,
                database_name=self._db_name,
                collection_name="chat_message_history",
            ),
        )

    def send_message(self, message: str) -> str:
        response = self._chat.invoke(
            {"answer": message},
            config=self._config,
        )

        return response

    @property
    def conversation_id(self) -> int:
        return self._conversation_id


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    from database import MongoDBConnector

    load_dotenv()

    chatbot = ConversationalChatBot(
        api_key=os.getenv("OPENAI_API_KEY"),
        conversation_id=2,
        conversation_user_level="advanced",
        conversation_difficulty="hard",
        conversation_topic=None,
        db_connector=MongoDBConnector(os.getenv("MONGODB_URI")),
    )

    bot_answer = chatbot.send_message(
        "Have we ever talked about the weather so far in our conversation?"
    )
    print(bot_answer)
