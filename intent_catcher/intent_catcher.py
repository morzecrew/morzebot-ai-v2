import json


class IntentCatcher:
    def __init__(self):
        pass

    def catch(self):
        pass


DATA_PATH = __file__ + "../data/"


class NatashaCatcher(IntentCatcher):
    def __init__(self, normal_sentence):
        self.normal_sentence = normal_sentence

    def catch(self):
        intents = self._read_json()

        for key, value in intents:
            # FIXME
            if value in self.normal_sentence.values():
                return key

    def _read_json(self):
        return json.loads(DATA_PATH)
