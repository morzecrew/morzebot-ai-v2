from navec import Navec
import numpy as np
from numpy.linalg import norm

from lib.preprocessing import Preprocessing
from lib.similarity import CosinSimilarity


class IntentCatcher:
    def __init__(self, user_sent, user_intent, emb: Preprocessing):  # user_sent = "hui", user_intent = {"hui":["hui and","chlen"], "":[]}
        self.user_sent = user_sent
        self.user_intents = user_intent
        self.emb = emb
        self.cos = CosinSimilarity()

    def __get_sent_emb(self):
        user_sent_emb = self.emb.preprocessing(self.user_sent)  # user = "Ну и хуита же" --> [0.1, 0.04 ... N]
        return user_sent_emb

    def __get_intent_emb(self):
        user_intent_emb = {}
        for key_intent, user_intent in self.user_intents.items():  # {"hui":["hui and","chlen"], "":[]} --> {"hui":[[0.03, 0.1],[0.02, 0.1]], "":[]}
            user_intent_emb[key_intent] = self.emb.preprocessing(user_intent)
        return user_intent_emb

    def get_intent(self):
        user_sent_emb = self.__get_sent_emb()
        user_intents_emb = self.__get_intent_emb()
        max_cos = -1
        for key_intent, user_intent_emb in user_intents_emb.items():
            for element in user_intent_emb:
                cosine = self.cos.cos_sim(user_sent_emb, element)
                print(cosine)
                if cosine > max_cos:
                    max_cos = cosine
                    return key_intent
