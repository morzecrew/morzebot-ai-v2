from razdel import tokenize
from lib.emb.preprocessing import Preprocessing
import numpy as np
from lib.similarity import Evaluation
# pip install transformers sentencepiece
import torch
from transformers import AutoTokenizer, AutoModel, AutoConfig
# BertTokenizer.from_pretrained(PATH, local_files_only=True)
import os

DATA_PATH = os.path.join(os.getcwd(), os.path.join(os.path.join("data", "bert"),'tiny_bert'))

config = AutoConfig.from_pretrained(os.path.join(DATA_PATH,'config.json'))
model = AutoModel.from_pretrained(os.path.join(DATA_PATH,'pytorch_model.bin'), config=config,
    local_files_only=True)
tokenizer = AutoTokenizer.from_pretrained(DATA_PATH,
                                          config=config, local_files_only=True)
# model.cuda()  # uncomment it if you have a GPU

class BERTModelWrapper:
    def __init__(self, model=model, tokenizer=tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    def encode(self,text):
        t = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = model(**{k: v.to(self.model.device) for k, v in t.items()})
        embeddings = model_output.last_hidden_state[:, 0, :]
        embeddings = torch.nn.functional.normalize(embeddings)
        return embeddings[0].cpu().numpy()

mod = BERTModelWrapper()

class BERTEmb(Preprocessing):
    def __init__(self, model_emb=mod):
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


# print(Evaluation().cos_dist(next(iter(BERTEmb().preprocessing("привет мир")["user_sent_and_emb"].values())),next(iter(BERTEmb().preprocessing("привет")["user_sent_and_emb"].values()))))