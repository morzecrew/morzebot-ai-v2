import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from chit_chat.chit_chat import ChitChat
from dotenv import load_dotenv

import os

load_dotenv()
TOKEN_HUGGINGFACE = os.getenv('TOKEN_HUGGINGFACE')
DO_SAMPLE = True
TOP_P = 0.95
NUM_RETURN_SEQUENCES = 3
REPETITION_PENALTY = 3.5
MAX_LENGTH = 128
TASK_PREFIX = ''

model = T5ForConditionalGeneration.from_pretrained('morzecrew/rut5-small-chit-chat-guffy-morze',
                                                   use_auth_token=TOKEN_HUGGINGFACE)
tokenizer = T5Tokenizer.from_pretrained('morzecrew/rut5-small-chit-chat-guffy-morze', use_auth_token=TOKEN_HUGGINGFACE)

class T5Model():
    def __init__(self, model=model, tokenizer=tokenizer):
        self.model = model
        self.tokenizer = tokenizer



chat_model = T5Model(model=model, tokenizer=tokenizer)


class T5ChitChat(ChitChat):
    def __init__(self, chatbot=chat_model, task_prefix =  TASK_PREFIX):
        super().__init__(chatbot)
        self.task_prefix = task_prefix

    def train(self):
        raise NotImplementedError

    def response(self, sentences, gpu=False, **kwargs):
        if gpu:
            device = "cuda:0"
        else:
            device = "cpu"
        self.chatbot.model = self.chatbot.model.to(device)
        self.chatbot.model.eval()
        if isinstance(sentences, list):
            response_list = []
            sentences = [self.task_prefix + phrase for phrase in sentences]
            for sentence in sentences:
                inputs = self.chatbot.tokenizer(sentence, return_tensors='pt').to(device)
                with torch.no_grad():
                    hypotheses = self.chatbot.model.generate(**inputs, **kwargs)
                response_list.append(self.chatbot.tokenizer.batch_decode(hypotheses, skip_special_tokens=True))
            return response_list

        sentences = self.task_prefix + sentences
        inputs = self.chatbot.tokenizer(sentences, return_tensors='pt').to(device)
        with torch.no_grad():
            hypotheses = self.chatbot.model.generate(**inputs, **kwargs)
        return self.chatbot.tokenizer.batch_decode(hypotheses, skip_special_tokens=True)

# print(T5ChitChat().response("пока", do_sample=True,
#                                  top_p=TOP_P,
#                                  num_return_sequences=NUM_RETURN_SEQUENCES,
#                                  repetition_penalty=REPETITION_PENALTY,
#                                  # num_beams = 4,
#                                  # num_beam_groups = 4,
#                                  # diversity_penalty = 2.0,
#                                  # top_k=50,
#                                  # early_stopping=True,
#                                  max_length=MAX_LENGTH))

