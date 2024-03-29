"""Chatbots for TeachMe project.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

from .PROMPTS import get_prompt


class BaseChatBot:
    def __init__(self, 
                 api_key: str, 
                 model_version: str = "gpt-3.5-turbo",
                 temperature: float = 0.2):
        self.api_key = api_key
        self.temperature = temperature

        self._chat_base = ChatOpenAI(
            model=model_version,
            api_key=self.api_key,
            temperature=temperature,
            # convert_system_message_to_human=True
        )

class ConversationalChatBot(BaseChatBot):
    def __init__(
        self,
        api_key: str,
        conversation_id: int,
        conversation_user_level: str = None,
        conversation_difficulty: str = None,
        conversation_topic: str = None,
        model_version: str = "gpt-3.5-turbo",
        temperature: float = 0.2
        ):
        super().__init__(api_key, model_version, temperature)

        self._conversation_id = conversation_id
        self._conversation_user_level = conversation_user_level
        self._conversation_difficulty = conversation_difficulty
        self._conversation_topic = conversation_topic
        self._chat = None
        self._config = None

    def load_chat_history(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", f"{get_prompt(prompt_name='CONVERSATIONAL_SYSTEM_PROMPT', user_level=self._conversation_user_level, conversation_difficulty=self._conversation_difficulty, conversation_topic=self._conversation_topic)}"),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{answer}"),
            ]
        )

        _chat_with_history = prompt | self._chat_base

        self._chat = RunnableWithMessageHistory(
            _chat_with_history,
            lambda session_id: SQLChatMessageHistory(
                session_id=session_id, connection_string="sqlite:///conversation_history.db"
            ),
            input_messages_key="answer",
            history_messages_key="history",
        )
        self._config = {"configurable": {"session_id": f"{self._conversation_id}"}}
    
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
    
    load_dotenv()
    
    chatbot = ConversationalChatBot(
        api_key=os.getenv("OPENAI_API_KEY"),
        conversation_id=1,
        conversation_user_level="intermediate",
        conversation_difficulty="medium",
        conversation_topic="Discussing the weather"
    )
    chatbot.load_chat_history()
    bot_answer = chatbot.send_message("How many messages did I send to you up to now?")
    print(bot_answer)