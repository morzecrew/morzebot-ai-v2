from razdel import tokenize
from navec import Navec
import numpy as np
from numpy.linalg import norm

path = 'navec_hudlit_v1_12B_500K_300d_100q.tar'
navec = Navec.load(path)

text = "СТОИТ Привет как дела"  # НУЖНО ЗНАКИ ПРИПИНАНИЯ УДАЛЯТЬ
us_intent = {"Приветствие": ["здравствуй", "хай"], "Цена": ["стоимость", "цена", "деньги", "стоит"]}


class PreprocessingIntents():
    def __init__(self, model_emb=navec):
        self.model_emb = model_emb

    def __tokenizer_sent(self, text: str):  # text = "abc bca ass" --> ["abc", "bca", "ass"]
        user_sent_tokens = list(tokenize(text))
        low_user_tokens = [_.text.lower() for _ in user_sent_tokens]
        return low_user_tokens

    def __tokenizer_intent(self,
                           text: list):  # text = ["abc abc", "ass ssa", "hui hui"] -->[["abc", "abc"],["ass", "ssa"],["hui", "hui"]]
        user_intent = [self.__tokenizer_sent(intent) for intent in text]
        return user_intent

    def __word_emb(self,
                   text: list):  # text = ["hui", "moy"] --> [array([0.12, 0.15, 0.45, ... N=300]), array([0.34, 0.15, 0.05, ... N=300])]
        word_emb = [self.model_emb[token] for token in text]
        return word_emb

    def __sent_emb(self, text_emb: list):
        # text_emb = [array([0.12, 0.15, 0.45, ... N=300]), array([0.34, 0.15, 0.05, ... N=300]),... M] --> [0.11, 0,3213, ... M*N]
        sent_emb = np.concatenate(text_emb, axis=None)
        return sent_emb

    def __sent_sum_emb(self, text_emb: list):
        # [array([0.12, 0.15, 0.45, ... N]), array([0.34, 0.15, 0.05, ... N]), ... M] --> 0.1232
        sent_sum_emb = [np.sum(text_emb, axis=None) / np.size(text), np.sum(text_emb, axis=None) / np.size(text)]
        return sent_sum_emb

    def preprocessing(self, text):
        if isinstance(text, str):
            tokens = self.__tokenizer_sent(text)
            word_emb = self.__word_emb(tokens)
            sent_emb = self.__sent_emb(word_emb)
            # sent_emb = self.__sent_sum_emb(word_emb)
        elif isinstance(text, list):
            tokens = self.__tokenizer_intent(text)
            word_emb = [self.__word_emb(element) for element in tokens]
            sent_emb = [self.__sent_emb(emb_element) for emb_element in word_emb]
            # sent_emb = [self.__sent_sum_emb(emb_element) for emb_element in word_emb]

        else:
            sent_emb = []
        # sent_sum_emb = self.__sent_sum_emb(word_emb)
        return sent_emb


class IntentCatcher():
    def __init__(self, user_sent, user_intent,
                 emb: PreprocessingIntents):  # user_sent = "hui", user_intent = {"hui":["hui and","chlen"], "":[]}
        self.user_sent = user_sent
        self.user_intents = user_intent
        self.emb = emb

    def __get_sent_emb(self):
        user_sent_emb = self.emb.preprocessing(self.user_sent)  # user = "Ну и хуита же" --> [0.1, 0.04 ... N]
        return user_sent_emb

    def __get_intent_emb(self):
        user_intent_emb = {}
        for key_intent, user_intent in self.user_intents.items():  # {"hui":["hui and","chlen"], "":[]} --> {"hui":[[0.03, 0.1],[0.02, 0.1]], "":[]}
            user_intent_emb[key_intent] = self.emb.preprocessing(user_intent)
        return user_intent_emb

    def __cos_dist(self, user_sent_emb, user_intent_emb):
        add = np.array([0] * abs((len(user_intent_emb) - len(user_sent_emb))))
        if len(user_sent_emb) > len(user_intent_emb):
            user_intent_emb = np.concatenate((user_intent_emb, add), axis=0)
        elif len(user_sent_emb) < len(user_intent_emb):
            user_sent_emb = np.concatenate((user_sent_emb, add), axis=0)
        # print("user_sent_emb= ", user_sent_emb)
        # print("user_intent_emb= ", user_intent_emb)
        # user_sent_emb = np.array(user_sent_emb).reshape(1, -1)
        # user_intent_emb = np.array(user_intent_emb).reshape(1,-1)
        cosin = np.dot(user_sent_emb, user_intent_emb) / (norm(user_sent_emb, ord=2) * norm(user_intent_emb, ord=2))
        # cosin = cosine_similarity(user_sent_emb, user_intent_emb)
        return cosin

    def get_intent(self):
        user_sent_emb = self.__get_sent_emb()
        user_intents_emb = self.__get_intent_emb()
        max_cos = -1
        for key_intent, user_intent_emb in user_intents_emb.items():
            for element in user_intent_emb:
                cosin = self.__cos_dist(user_sent_emb, element)
                print(cosin)
                if cosin > max_cos:
                    max_cos = cosin
                    return key_intent
