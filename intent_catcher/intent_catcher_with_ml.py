from intent_catcher.get_intents import GetIntentsEmb
from lib.emb.preprocessing import Preprocessing
from lib.models_wrapper import ModelsWrapper
from lib.similarity import Evaluation
from intent_catcher.intent_catcher import IntentCatcher


class IntentCatcherML(IntentCatcher):
    def __init__(self, user_sent, emb: Preprocessing, model: ModelsWrapper):
        super().__init__(user_sent, emb)
        self.cos = Evaluation()
        self.user_sent = user_sent
        self.cos = Evaluation()
        self.user_intents = GetIntentsEmb(emb)
        self.model = model

    def get_intent(self):
        user_sent_emb = self.__get_sent_emb()
        user_intents_emb = self.user_intents.get_intent_emb()
        score = -1
        prediction = self.model.predict(emb=user_sent_emb['user_sent_and_emb'][self.user_sent].reshape(1, -1))
        intent = list(user_intents_emb.keys())[prediction['label']]
        score = prediction['prob']

        if len(intent) > 0:
            result = self.__get_word(intent, user_sent_emb, user_intents_emb, score)
        else:
            result = {"intent": intent, "sent_score": score, "user_sent": "", "max_cosine_word": -1}
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
        return {"intent": intent_key, "sent_score": cos_sent, "user_sent": word, "max_cosine_word": max_cos}

    def __get_sent_emb(self):
        user_sent_emb = self.emb.preprocessing(self.user_sent)
        return user_sent_emb
