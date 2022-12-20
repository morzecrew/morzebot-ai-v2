class SpellSheckerWrapper():
    def __init__(self, model):
        self.model = model


    def correct(self, sentence):
        raise NotImplementedError
