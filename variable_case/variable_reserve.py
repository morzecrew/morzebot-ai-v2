class Catcher:
    def __init__(self):
        pass

    def get_variable(self):
        raise NotImplementedError


class VaraibleReserve(Catcher):
    def __init__(self, intent: dict, normalize_doc):
        super().__init__()
        self.intent_head_id = intent
        self.normalize_doc = normalize_doc

    def get_var(self):

    def _get_variable_first(self):
        values = []
        for token in self.normalize_doc.tokens:
            if token.head_id == token_id:
                values.append(token)
        return values

    def _get_variable_second(self):
        values = []
        for token in self.normalize_doc.tokens:
            if token.head_id == token_id:
                values.append(token)
        return values

