from threading import Lock
import json
import os

from data.path_to_data import get_data_path
from lib.emb.preprocessing import Preprocessing


class SingletonBase(type):
    __instances = {}
    __lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            if cls not in cls.__instances:
                cls.__instances[cls] = super(SingletonBase, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]

    def __del__(self):
        SingletonBase.__instances = None


DATA_PATH = os.path.join(get_data_path(), "user_intents.json")


def read_json():
    file = open(DATA_PATH, encoding='UTF-8')
    return json.loads(file.read())


class GetIntentsEmb(metaclass=SingletonBase):
    def __init__(self, emb: Preprocessing):
        self.user_intents = read_json()
        self.emb = emb

    def get_intent_emb(self):
        user_intent_emb = {}
        for key_intent, user_intent in self.user_intents.items():  # {"hui":["hui and","chlen"], "":[]} --> {"hui":[[0.03, 0.1],[0.02, 0.1]], "":[]}
            user_intent_emb[key_intent] = self.emb.preprocessing(user_intent)
        return user_intent_emb
