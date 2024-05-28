"""Module for managing the chatbots for the conversations."""

from threading import Lock, Thread
from time import sleep
from os import getenv
from bson.errors import InvalidId


from . import ConversationalChatBot
from ..database import MongoDB
from ..log import *


class ChatbotManager:
    """Manages the chatbots for the conversations.

    :ivar chatbots: dictionary containing the chatbots for the conversations
    :vartype chatbots: dict
    :ivar dict_lock: lock for the chatbots dictionary
    :vartype dict_lock: Lock
    :ivar max_idle_time: idling time (in seconds) for the thread checking the chatbots. Defaults to 10 seconds.
    :vartype max_idle_time: int, Optional
    :ivar heartbeat_thread: thread for the heartbeat
    """

    def __init__(self, max_idle_time: int = 10):
        # self.chatbots : SynchronizedDict = SynchronizedDict()
        self.chatbots = dict()
        self.dict_lock = Lock()
        self.max_idle_time = max_idle_time

        def run_check_idle():
            idle_time = self.max_idle_time
            while True:
                sleep(idle_time)
                self.check_idle()

        self.heartbeat_thread = Thread(target=run_check_idle)
        # start interval

    def start_heartbeat(self):
        """Start the heartbeat thread that checks if the chatbots are idle."""
        self.heartbeat_thread.start()

    def init_chatbot(self, cid: str, db: MongoDB, logger: Logger) -> tuple[int, str]:
        """Initialize the chatbot for the specified conversation.

        If the conversation_id is of an invalid format, the function returns a 400 status code and an error message.
        If the conversation is not found in the database, the function returns a 400 status code and an error message because
        the conversation must be created before initializing it.
        If the chatbot is already initialized, the function returns a 200 status code and a success message.
        Otherwise a new chatbot is created and added to the chatbot manager, finally returning a 200 status code and a success message.

        :param cid: id of the conversation to initialize
        :type cid: str
        :param db: database instance containing the conversations data
        :type db: MongoDB
        :param logger: logger instance to log messages
        :type logger: Logger
        :return: Returns a tuple containing the status code and the response message.
        :rtype: tuple[int, str]
        """
        conversations_collection = db.get_collection("conversations")

        try:
            conversation = conversations_collection.find_by_id(cid)
        except InvalidId:
            logger.log(Log(LogType.ERROR, f"Invalid conversation_id: {cid}"))
            return 400, "Invalid conversation_id"

        if conversation is None:
            logger.log(Log(LogType.ERROR, f"Conversation not found: {cid}"))
            return (
                400,
                "Conversation not found. You must create a conversation before initializing it.",
            )

        # Initializing the Chatbot for the conversation if not already initialized
        cb = self.get_chatbot(cid)
        if not cb:
            logger.log(
                Log(
                    log_type=LogType.INFO,
                    message=f"Initializing conversation with id {cid}",
                )
            )
            self.add_chatbot(
                cid,
                ConversationalChatBot(
                    api_key=getenv("OPENAI_API_KEY"),
                    conversation_id=cid,
                    db=db,
                    logger=logger,
                ),
            )

        return 200, "Conversation initialized successfully"

    def check_idle(self) -> None:
        """Check if the chatbots are idle and, if so, deactivate them and remove them from the list."""
        with self.dict_lock:
            for cid, chatbot in self.chatbots.items():
                if chatbot.is_idle:
                    chatbot.deactivate()
                    del self.chatbots[cid]

    def get_chatbot(self, cid: str) -> ConversationalChatBot:
        """Get the chatbot for the specified conversation.

        :param cid: id of the conversation
        :type cid: str
        :return: Returns the chatbot for the specified conversation or None if the conversation is not initialized.
        :rtype: ConversationalChatBot
        """
        with self.dict_lock:
            return self.chatbots.get(cid, None)

    def add_chatbot(self, cid: str, chatbot: ConversationalChatBot) -> None:
        """Add a chatbot to the chatbot manager.

        :param cid: id of the conversation managed by the chatbot
        :type cid: str
        :param chatbot: the chatbot to add
        :type chatbot: ConversationalChatBot
        """
        with self.dict_lock:
            self.chatbots[cid] = chatbot

    def send_message_to_chatbot(self, cid: str, message: str) -> tuple[int, str]:
        """Send a message to the chatbot in the specified conversation.

        :param cid: id of the conversation in which the message is sent
        :type cid: str
        :param message: the message to send to the chatbot coming from the user
        :type message: str
        :return: Returns a tuple containing the status code and the response message.
        The response message is the chatbot's response to the user message or an error
        message in case the conversation is not initialized.
        :rtype: tuple[int, str]
        """
        chatbot = self.get_chatbot(cid)

        if chatbot is None:
            return (
                400,
                "Chatbot not initialized. Before sending messages, you must initialize the conversation. See /initialize-conversation.",
            )

        response = chatbot.send_message(message)
        response_message = response["output"]
        return 200, response_message

    def end_chatbot(self, cid: str, db: MongoDB, logger: Logger) -> None:
        """End the chatbot for the specified conversation.

        :param cid: id of the conversation to end
        :type cid: str
        :param db: database instance containing the conversations data
        :type db: MongoDB
        :param logger: logger instance to log messages
        :type logger: Logger
        """
        chatbot = self.get_chatbot(cid)
        if chatbot:
            chatbot.deactivate()
            del self.chatbots[cid]

        # Update the conversation in the database
        # TODO: get messages and create a new EndedConversation object
        conversations_collection = db.get_collection("conversations")
