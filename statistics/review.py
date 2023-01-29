import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

TOKEN_HUGGINGFACE = os.getenv("TOKEN_HUGGINGFACE")

MODEL_NAME = 'morzecrew/rubert-tiny-review'

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=TOKEN_HUGGINGFACE)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, use_auth_token=TOKEN_HUGGINGFACE)
if torch.cuda.is_available():
    model.cuda()


class BERTModelWrapper:
    def __init__(self, model=model, tokenizer=tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def classify(self, text):
        with torch.no_grad():
            inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(self.model.device)
            proba = torch.sigmoid(self.model(**inputs).logits).cpu().numpy()[0]

        return proba


model_bert = BERTModelWrapper()


class Reviewer:
    def __init__(self, model=model_bert):
        self.model = model

    def get_sentiment(self, text, return_type='label'):
        """ Calculate sentiment of a text. `return_type` can be 'label', 'score' or 'proba' """
        proba = self.model.classify(text)
        if return_type == 'label':
            return model.config.id2label[proba.argmax()]
        elif return_type == 'score':
            return proba.argmax()
        return proba

# text = 'Пноравился'
# import time
# time_s = time.time()
# print(Reviewer().get_sentiment(text, 'label'))  # negative
# print(time.time() - time_s)  # 0.005s
# # score the text on the scale from -1 (very negative) to +1 (very positive)
# print(Reviewer().get_sentiment(text, 'score'))
# # calculate probabilities of all labels
# print(Reviewer().get_sentiment(text, 'proba'))
