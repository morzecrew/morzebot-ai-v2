class ChitChat():
    def __init__(self, chatbot):
        self.chatbot = chatbot

    def train(self):
        raise NotImplementedError

    def response(self, sentence):
        raise NotImplementedError
