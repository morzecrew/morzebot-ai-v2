class VariableCatcher:
    def __init__(self, intent: dict, normalize_doc):
        self.intent_head = intent
        self.normalize_doc = normalize_doc

    def _get_token_id(self):
        for token in self.normalize_doc.tokens:
            if self.intent_head["user_sent"] == token.text:
                return token.id
        return ""

    def _get_var_on_level(self, token_id):
        for token in self.normalize_doc.tokens:
            if token.head_id == token_id:
                return {"value": token.lemma, "token_id": token.id}
        return {"value": "", "token_id": ""}

    def get_variable(self):
        raise NotImplementedError
