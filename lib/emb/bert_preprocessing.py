from razdel import tokenize
import time
from lib.emb.preprocessing import Preprocessing

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel, AutoConfig
import os


def get_models_path(name):
    model_path = {"tiny-bert": "cointegrated/rubert-tiny", "tiny-bert2": "cointegrated/rubert-tiny2",
                  "LaBSE-en-ru": "cointegrated/LaBSE-en-ru", "rubert-tiny2-tuned": "morzecrew/rubert-tiny2-finetuned-embedding"}
    return model_path[name]


class PretrainedModels:
    def __init__(self):
        pass

    def tokenizer(self, model_name: str, token=False):
        model_path = get_models_path(model_name)
        try:
            if token:
                tokenizer_model = AutoTokenizer.from_pretrained(model_path, local_files_only=True, use_auth_token=os.getenv("HUGFACE_TOKEN"))
            else:
                tokenizer_model = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        except:
            if token:
                tokenizer_model = AutoTokenizer.from_pretrained(model_path, use_auth_token=os.getenv("HUGFACE_TOKEN"))
            else:
                tokenizer_model = AutoTokenizer.from_pretrained(model_path)
        return tokenizer_model

    def model(self, model_name: str, token=False):
        model_path = get_models_path(model_name)
        try:
            if token:
                emb_model = AutoModel.from_pretrained(model_path, local_files_only=True, use_auth_token=os.getenv("HUGFACE_TOKEN"))
            else:
                emb_model = AutoModel.from_pretrained(model_path, local_files_only=True)
        except:
            if token:
                emb_model = AutoModel.from_pretrained(model_path, use_auth_token=os.getenv("HUGFACE_TOKEN"))
            else:
                emb_model = AutoModel.from_pretrained(model_path)
        return emb_model


class BERTModelWrapper:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def encode(self, text):
        t = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**{k: v.to(self.model.device) for k, v in t.items()})
        embeddings = model_output.last_hidden_state[:, 0, :]
        embeddings = torch.nn.functional.normalize(embeddings)
        # model.cuda()  # uncomment it if you have a GPU
        return embeddings[0].cpu().numpy()


class BERTEmb(Preprocessing):
    def __init__(self, model_emb: BERTModelWrapper):
        super().__init__()
        self.model_emb = model_emb

    def preprocessing(self, text):
        if isinstance(text, str):
            tokens = self.__tokenizer_sent(text)  # "Привет как дела" --> ["привет","как","дела"]
            word_emb = self.__word_emb(tokens)  # ["привет","как","дела"] --> [[0.1, 0.1...], [...], [...]]
            sent_emb = self.__sent_emb(text)  # [[0.1, 0.1...], [...], [...]] --> [0.1, 0.03, ...]
            word_and_emb = {}
            for count in range(len(tokens)):
                word_and_emb[tokens[count]] = word_emb[
                    count]  # Пофиксить если у нас одинаковые слова в предложении: "Привет, привет" оно перезаписывает
            result = {"user_word_and_emb": word_and_emb, "user_sent_and_emb": {text: sent_emb}}

        elif isinstance(text, list):
            sent_emb = [self.__sent_emb(emb_element) for emb_element in text]
            result = sent_emb

        else:
            result = []
        return result

    def __tokenizer_sent(self, text: str):
        user_sent_tokens = list(tokenize(text))
        low_user_tokens = [_.text.lower() for _ in user_sent_tokens]
        return low_user_tokens

    def __tokenizer_intent(self, text: list):
        user_intent = [self.__tokenizer_sent(intent) for intent in text]
        return user_intent

    def __word_emb(self, text: list):
        samp = self.model_emb.encode('навек')
        word_emb = []
        for token in text:
            try:
                word_emb.append(self.model_emb.encode(token))
            except:
                word_emb.append(np.array([0] * len(samp)))
        return word_emb

    def __sent_emb(self, text_emb):
        if isinstance(text_emb, list):
            if any(isinstance(val, str) for val in text_emb):
                sent_emb = self.model_emb.encode(text_emb)
            else:
                sent_emb = np.sum(text_emb, axis=0) / np.size(text_emb, 0)
        elif isinstance(text_emb, str):
            sent_emb = self.model_emb.encode(text_emb)

        return sent_emb
