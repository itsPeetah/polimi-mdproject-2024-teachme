from threading import Lock, Thread
from time import sleep


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

    def init_chatbot(self, cid):
        with self.dict_lock:
            # TODO check if exists
            # cb = Chatbot()
            # self.chatbots[cid] = cb
            pass

    def check_idle(self):
        with self.dict_lock:
            for cid, chatbot in self.chatbots.items():
                # if not chatbot.isActive or chatbot.is_idle:
                # chatbot.turn_off()
                # del self.chatbots[cid]
                pass
