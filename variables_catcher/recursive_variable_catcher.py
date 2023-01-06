class IdCatcher:
    def __init__(self):
        pass

    def get_variable(self):
        raise NotImplementedError


class RecVariableCatcher(IdCatcher):
    def __init__(self, intent: dict, normalize_doc):
        super().__init__()
        self.intent_head_id = intent
        self.normalize_doc = normalize_doc
        self.value_rec = {}
        self.count = 1
        self.depth_recurs = 3

    def get_variable(self):

        values = self.__recursive_search_variable(self.intent_head_id["token_id"])
        res = {"intent": self.intent_head_id["key"], "payload": {self.intent_head_id["user_sent"]: {"values": values}}}

        return res

    def __recursive_search_variable(self, token_id: str):

        if self.count < self.depth_recurs:
            for token in self.normalize_doc.tokens:
                if token.head_id == token_id:
                    self.value_rec["level_" + str(self.count)] = token.lemma
                    token_id = token.id
                    self.count = self.count + 1
                    self.__recursive_search_variable(token_id)
                else:
                    self.value_rec["level_" + str(self.count)] = ""

        return self.value_rec
