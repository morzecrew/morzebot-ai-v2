import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from chit_chat.chit_chat import ChitChat
from dotenv import load_dotenv

import os

load_dotenv()
TOKEN_HUGGINGFACE = os.getenv('TOKEN_HUGGINGFACE')

device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'

model = T5ForConditionalGeneration.from_pretrained('morzecrew/rut5-small-chit-chat-guffy-morze',
                                                   use_auth_token=TOKEN_HUGGINGFACE)
tokenizer = T5Tokenizer.from_pretrained('morzecrew/rut5-small-chit-chat-guffy-morze', use_auth_token=TOKEN_HUGGINGFACE)
model = model.to(device)


class T5Model():
    def __init__(self, model=model, tokenizer=tokenizer,
                 do_sample=True, top_p=0.4, num_return_sequences=3,
                 repetition_penalty=2.5,
                 max_length=32):
        self.model = model
        self.tokenizer = tokenizer
        self.do_sample = do_sample
        self.top_p = top_p
        self.num_return_sequences = num_return_sequences
        self.repetition_penalty = repetition_penalty
        self.max_length = max_length


chat_model = T5Model(model=model, tokenizer=tokenizer,
                     do_sample=True, top_p=0.95, num_return_sequences=3,
                     repetition_penalty=3.5,
                     max_length=128)


class T5ChitChat(ChitChat):
    def __init__(self, chatbot=chat_model):
        super().__init__(chatbot)

    def train(self):
        raise NotImplementedError

    def response(self, sentence):
        inputs = self.chatbot.tokenizer(sentence, return_tensors='pt')
        with torch.no_grad():
            hypotheses = self.chatbot.model.generate(
                **inputs,
                do_sample=self.chatbot.do_sample,
                top_p=self.chatbot.top_p,
                num_return_sequences=self.chatbot.num_return_sequences,
                # repetition_penalty=self.chatbot.repetition_penalty,
                max_length=self.chatbot.max_length,
                top_k=50
            )

        if len(hypotheses) == 1:
            return self.chatbot.tokenizer.decode(hypotheses[0], skip_special_tokens=True)

        response_list = []
        for h in hypotheses:
            response_list.append(self.chatbot.tokenizer.decode(h, skip_special_tokens=True))
        return response_list

# print(T5ChitChat().response("пока"))
