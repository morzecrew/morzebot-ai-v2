import json
import os


from lib.preprocessing import Preprocessing
from lib.similarity import Evaluation

DATA_PATH = os.path.join(os.getcwd(),os.path.join("data", "user_intents.json"))


def _read_json():
    file = open(DATA_PATH, encoding='UTF-8')
    return json.loads(file.read())


class IntentCatcher:
    def __init__(self, user_sent, emb: Preprocessing):  # user_sent = "hui", user_intent = {"hui":["hui and","chlen"], "":[]}
        self.user_sent = user_sent
        self.user_intents = _read_json()
        self.emb = emb
        self.cos = Evaluation()
        self.max_cos = 0.6

    def __get_sent_emb(self):
        user_sent_emb = self.emb.preprocessing(self.user_sent)  # user = "Ну и хуита же" --> [0.1, 0.04 ... N]
        return user_sent_emb

    # def __get_intent_emb(self):
    #     user_intent_emb = {}
    #     for key_intent, user_intent in self.user_intents.items():  # {"hui":["hui and","chlen"], "":[]} --> {"hui":[[0.03, 0.1],[0.02, 0.1]], "":[]}
    #         user_intent_emb[key_intent] = self.emb.preprocessing(user_intent)
    #     return user_intent_emb
    def _get_intent_emb(self):
        user_intent_emb = {}
        for key_intent, user_intent in self.user_intents.items():  # {"hui":["hui and","chlen"], "":[]} --> {"hui":[[0.03, 0.1],[0.02, 0.1]], "":[]}
            emb = self.emb.preprocessing(user_intent)

            user_intent_emb[key_intent] = self.emb.preprocessing(user_intent)
        return user_intent_emb


    def get_intent(self):
        user_sent_emb = self.__get_sent_emb()
        user_intents_emb = self.__get_intent_emb()
        for key_intent, user_intent_emb in user_intents_emb.items():
            for element in user_intent_emb:
                cosine = self.cos.cos_dist(user_sent_emb, element)
                if cosine > self.max_cos:
                    result = self.__get_id(key_intent,user_sent_emb,user_intents_emb )
                    return result

    def __get_id(self, intent_key, user_sent_emb, user_intents_emb):
        user_sent_split = self.user_sent.split()
        for iter, token_emb in enumerate(user_sent_emb):
            for intent_emb in user_intents_emb[intent_key]:
                cosine = self.cos.cos_dist(intent_emb, token_emb)
                if cosine > self.max_cos:
                    return {"intent": intent_key, "user_sent": user_sent_split[iter]}


#по эмбедингам найти косинуснове расстояние а потом вернуть индекс элемента