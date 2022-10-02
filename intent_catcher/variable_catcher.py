import json
import os


class IdCatcher:
    def __init__(self):
        pass

    def catch(self):
        raise NotImplementedError


DATA_PATH = os.getcwd() + "\\data\\user_intents.json"


def _read_json():
    file = open(DATA_PATH, encoding='UTF-8')
    return json.loads(file.read())


class VariableCatcher(IdCatcher):
    def __init__(self, intent: dict, normalize_doc):
        super().__init__()
        self.intent_head_id = intent
        self.normalize_doc = normalize_doc

    def compare_id(self):
        value_rec = {}
        for token in self.normalize_doc.tokens:
            if token.head_id == self.intent_head_id["token_id"]:
                value_rec["intents"] = self.intent_head_id["key"]
                value_rec["values"] = token.lemma
            else:
                value_rec["intents"] = self.intent_head_id["key"]
                value_rec["values"] = ""
        return value_rec

