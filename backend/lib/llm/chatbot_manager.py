from threading import Lock, Thread
from time import sleep
from bson.errors import InvalidId
from . import ConversationalChatBot
from ..database import MongoDB
from ..log import *
from os import getenv


class ChatbotManager:
    def __init__(self, max_idle_time: bool):
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
        self.heartbeat_thread.start()

    def init_chatbot(self, cid, db: MongoDB, logger: Logger):
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

    def check_idle(self):
        with self.dict_lock:
            for cid, chatbot in self.chatbots.items():
                # if not chatbot.isActive or chatbot.is_idle:
                # chatbot.turn_off()
                # del self.chatbots[cid]
                pass

    def get_chatbot(self, cid):
        with self.dict_lock:
            return self.chatbots.get(cid, None)

    def add_chatbot(self, cid: str, chatbot: ConversationalChatBot):
        with self.dict_lock:
            self.chatbots[cid] = chatbot
