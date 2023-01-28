class ModelsWrapper:
    def __init__(self):
        pass

    def save(self, filename):
        return NotImplementedError

    def load(self, filename):
        raise NotImplementedError

    def predict(self, emb):
        raise NotImplementedError
