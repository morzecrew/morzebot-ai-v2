from intent_catcher.get_intents import GetIntentsEmb
from lib.emb.preprocessing import Preprocessing
from lib.similarity import Evaluation


class IntentCatcher:
    def __init__(self, user_sent, emb: Preprocessing):
        self.user_sent = user_sent
        self.emb = emb
        self.cos = Evaluation()
        self.user_intents = GetIntentsEmb(emb)

    def get_intent(self):
        user_sent_emb = self.__get_sent_emb()
        user_intents_emb = self.user_intents.get_intent_emb()
        threshold = 0.2
        cosine = []
        max_cos = -1
        intent = ""
        for key_intent, user_intent_emb in user_intents_emb.items():
            for element in user_intent_emb:
                cosine.append(self.cos.cos_dist(user_sent_emb['user_sent_and_emb'][self.user_sent], element))
            max_simil = max(cosine)
            if max_simil > max_cos and max_simil > threshold:
                max_cos = max_simil
                intent = key_intent
        if len(intent) > 0:
            result = self.__get_word(intent, user_sent_emb, user_intents_emb, max_cos)
        else:
            result = {"intent": intent, "max_cosine_sent": max_cos, "user_sent": "", "max_cosine_word": -1}
        return result

    def __get_word(self, intent_key, user_sent_emb, user_intents_emb, cos_sent):
        max_cos = -1
        word = ""
        for words, token_emb in user_sent_emb["user_word_and_emb"].items():
            for intent_emb in user_intents_emb[intent_key]:
                cosine = self.cos.cos_dist(intent_emb, token_emb)
                if cosine > max_cos and cosine > 0.5:
                    max_cos = cosine
                    word = words
        return {"intent": intent_key, "max_cosine_sent": cos_sent, "user_sent": word, "max_cosine_word": max_cos}

    def __get_sent_emb(self):
        user_sent_emb = self.emb.preprocessing(self.user_sent)
        return user_sent_emb
