from variables_catcher.base_veriables_catcher import VariableCatcher


class ReserveCatcher(VariableCatcher):
    def __init__(self, intent: dict, normalize_doc):
        super().__init__(intent, normalize_doc)

    def get_variable(self):
        token_id = self._get_token_id()
        var_on_first_level = self._get_var_on_level(token_id)
        var_on_second_level = self._get_var_on_level(var_on_first_level["token_id"])
        result = {"intent": self.intent_head["intent"], "payload": {
            self.intent_head["user_sent"]: {"variables": [var_on_first_level["value"], var_on_second_level["value"]]}}}
        return result
