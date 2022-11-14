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

    def __get_sent_emb(self):
        user_sent_emb = self.emb.preprocessing(self.user_sent)  # user = "Ну и хуита же" --> {'user_word': {'ну': [...], 'и': [...], 'хуита': [...]}, 'user_sent': {'Ну и хуита же': [...]}}
        return user_sent_emb

    def __get_intent_emb(self):
        user_intent_emb = {}
        for key_intent, user_intent in self.user_intents.items():  # {"hui":["hui and","chlen"], "":[]} --> {"hui":[[0.03, 0.1],[0.02, 0.1]], "":[]}
            user_intent_emb[key_intent] = self.emb.preprocessing(user_intent)
        return user_intent_emb

    def get_intent(self):
        user_sent_emb = self.__get_sent_emb()
        user_intents_emb = self.__get_intent_emb()
        cosine = []
        max_cos = -1
        intent = ""
        for key_intent, user_intent_emb in user_intents_emb.items():
            for element in user_intent_emb:
                cosine.append(self.cos.cos_dist(user_sent_emb['user_sent_and_emb'][self.user_sent], element))
            max_simil = max(cosine)
            if max_simil > max_cos:
                max_cos = max_simil
                intent = key_intent
        result = self.__get_word(intent, user_sent_emb, user_intents_emb)
        return result

    def __get_word(self, intent_key, user_sent_emb, user_intents_emb):
        max_cos = -1
        for words, token_emb in user_sent_emb["user_word_and_emb"].items():
            for intent_emb in user_intents_emb[intent_key]:
                cosine = self.cos.cos_dist(intent_emb, token_emb)
                if cosine > max_cos:
                    max_cos = cosine
                    word = words
        return {"intent": intent_key, "user_sent": word, "max_cosine": max_cos}


