from razdel import tokenize
import numpy as np


class Preprocessing:
    def __init__(self, model_emb=None):
        self.model_emb = model_emb

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

    def __tokenizer_sent(self, text: str):  # text = "abc bca ass" --> ["abc", "bca", "ass"]
        user_sent_tokens = list(tokenize(text))
        low_user_tokens = [_.text.lower() for _ in user_sent_tokens]
        return low_user_tokens

    def __tokenizer_intent(self, text: list):  # text = ["abc abc", "ass ssa", "hui hui"] -->[["abc", "abc"],["ass", "ssa"],["hui", "hui"]]
        user_intent = [self.__tokenizer_sent(intent) for intent in text]
        return user_intent

    def __word_emb(self, text: list):  # text = ["hui", "moy"] --> [array([0.12, 0.15, 0.45, ... N=300]), array([0.34, 0.15, 0.05, ... N=300])]
        samp = self.model_emb['навек']
        try:
            word_emb = [self.model_emb[token] for token in text]
        except:
            word_emb = [0] * len(samp)
        return word_emb

    def __sent_emb(self, text_emb: list):
        # text_emb = [array([0.12, 0.15, 0.45, ... N=300]), array([0.34, 0.15, 0.05, ... N=300]),... M] --> [0.11, 0,3213, ... M*N]
        # sent_emb = np.concatenate(text_emb, axis=None)
        sent_emb = np.sum(text_emb, axis=0) / np.size(text_emb, 0)
        return sent_emb
