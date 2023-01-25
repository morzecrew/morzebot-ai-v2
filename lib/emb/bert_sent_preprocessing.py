import time

from razdel import tokenize
from sentence_transformers import SentenceTransformer
import numpy as np

#from data.models.path_to_models import path_to_models
from lib.emb.preprocessing import Preprocessing
from lib.similarity import Evaluation
import os

# DATA_PATH = r'C:\Users\Asus\morzebot-ai-v2\data\models\tiny_bert2'
model_name = "tiny_bert"  # Другие имена моделей "tiny_bert", "LaBSE-en-ru"
DATA_PATH = os.path.join(path_to_models(), model_name)

model = SentenceTransformer(DATA_PATH)


class BERTSentEmb(Preprocessing):
    def __init__(self, model_emb=model):
        super().__init__()
        self.model_emb = model_emb

    def preprocessing(self, text):
        if isinstance(text, str):
            tokens = self.__tokenizer_sent(text)  # "Привет как дела" --> ["привет","как","дела"]
            word_emb = self.__word_emb(tokens)  # ["привет","как","дела"] --> [[0.1, 0.1...], [...], [...]]
            sent_emb = self.__sent_emb(text)  # [[0.1, 0.1...], [...], [...]] --> [0.1, 0.03, ...]
            word_and_emb = {}
            for count in range(len(tokens)):
                word_and_emb[tokens[count]] = word_emb[count]
            result = {"user_word_and_emb": word_and_emb, "user_sent_and_emb": {text: sent_emb}}

        elif isinstance(text, list):
            sent_emb = [self.__sent_emb(emb_element) for emb_element in text]
            result = sent_emb

        else:
            result = []
        # print(result)
        return result  # sent_emb

    def __tokenizer_sent(self, text: str):  # text = "abc bca ass" --> ["abc", "bca", "ass"]
        user_sent_tokens = list(tokenize(text))
        low_user_tokens = [_.text.lower() for _ in user_sent_tokens]
        return low_user_tokens

    def __tokenizer_intent(self,
                           text: list):  # text = ["abc abc", "ass ssa", "hui hui"] -->[["abc", "abc"],["ass", "ssa"],["hui", "hui"]]
        user_intent = [self.__tokenizer_sent(intent) for intent in text]
        return user_intent

    # FIX ME
    def __word_emb(self,
                   text: list):  # text = ["hui", "moy"] --> [array([0.12, 0.15, 0.45, ... N=300]), array([0.34, 0.15, 0.05, ... N=300])]
        samp = self.model_emb.encode('навек')
        try:
            word_emb = [self.model_emb.encode(token) for token in text]
        except:
            word_emb = [0] * len(samp)
        return word_emb

    def __sent_emb(self, text_emb):
        # text_emb = [array([0.12, 0.15, 0.45, ... N=300]), array([0.34, 0.15, 0.05, ... N=300]),... M] --> [0.11, 0,3213, ... M*N]
        # sent_emb = np.concatenate(text_emb, axis=None)
        if isinstance(text_emb, list):
            if any(isinstance(val, str) for val in text_emb):
                sent_emb = self.model_emb.encode(text_emb)
            else:
                sent_emb = np.sum(text_emb, axis=0) / np.size(text_emb, 0)
        elif isinstance(text_emb, str):
            sent_emb = self.model_emb.encode(text_emb)

        return sent_emb

