from chit_chat.chit_chat import ChitChat
from chatterbot import ChatBot
from chatterbot.languages import RUS
from chatterbot.trainers import ChatterBotCorpusTrainer


# python -m spacy download ru_core_news_sm

# spacy bug fix
class RUSSM:
    ISO_639_1 = 'ru_core_news_sm'


chat_model = ChatBot("Morze", language=RUS, tagger_language=RUSSM)


class ChatterBot(ChitChat):
    def __init__(self, chatbot=chat_model):
        super().__init__(chatbot)

    def train(self):
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        trainer.train("chatterbot.corpus.russian.conversations")

    def response(self, sentence):
        return self.chatbot.get_response(sentence)
