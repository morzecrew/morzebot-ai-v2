class SpellSheckerWrapper():
    def __init__(self, model):
        self.model = model
        pass

    def correct(self, sentence):
        return self.model.correct(sentence)
