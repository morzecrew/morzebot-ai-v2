from razdel import tokenize
import numpy as np
from lib.emb.preprocessing import Preprocessing
import pymorphy2


class NavecEmb(Preprocessing):
    def __init__(self, model_emb=None):
        super().__init__()
        self.model_emb = model_emb

    def preprocessing(self, text):
        if isinstance(text, str):
            tokens = self.__tokenizer_sent(text)  # "Привет как дела" --> ["привет","как","дела"]
            word_emb = self.__word_emb(tokens)  # ["привет","как","дела"] --> [[0.1, 0.1...], [...], [...]]
            sent_emb = self.__sent_emb(word_emb)  # [[0.1, 0.1...], [...], [...]] --> [0.1, 0.03, ...]
            word_and_emb = {}
            for count in range(len(tokens)):
                word_and_emb[tokens[count]] = word_emb[count]
            result = {"user_word_and_emb": word_and_emb, "user_sent_and_emb": {text: sent_emb}}

        elif isinstance(text, list):
            tokens = self.__tokenizer_intent(text)
            word_emb = [self.__word_emb(element) for element in tokens]
            sent_emb = [self.__sent_emb(emb_element) for emb_element in word_emb]
            result = sent_emb

        else:
            result = []

        return result

    def __tokenizer_sent(self, text: str):  # text = "abc bca ass" --> ["abc", "bca", "ass"]
        user_sent_tokens = list(tokenize(text))
        low_user_tokens = [_.text.lower() for _ in user_sent_tokens]
        return low_user_tokens

    def __tokenizer_intent(self, text: list):  # text = ["abc abc", "ass ssa", "hui hui"] -->[["abc", "abc"],["ass", "ssa"],["hui", "hui"]]
        user_intent = [self.__tokenizer_sent(intent) for intent in text]
        return user_intent

    def __word_normalizer(self, text):
        morph = pymorphy2.MorphAnalyzer()
        return morph.parse(text)[0].normal_form

    def __word_emb(self,text: list):  # text = ["hui", "moy"] --> [array([0.12, 0.15, 0.45, ... N=300]), array([0.34, 0.15, 0.05, ... N=300])]
        samp = self.model_emb['навек']
        word_emb = []
        for token in text:
            try:
                word_emb.append(self.model_emb[token])
            except:
                word_emb.append(np.array([0] * len(samp)))
        return word_emb

    def __sent_emb(self, text_emb):
        if isinstance(text_emb, list):
            sent_emb = np.sum(text_emb, axis=0) / np.size(text_emb, 0)
        return sent_emb
