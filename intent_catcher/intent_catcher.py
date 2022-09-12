import json
import os


class IntentCatcher:
    def __init__(self):
        pass

    def catch(self):
        raise NotImplementedError


DATA_PATH = os.getcwd() + "\\data\\user_intents.json"


def _read_json():
    file = open(DATA_PATH, encoding='UTF-8')
    return json.loads(file.read())


class NatashaCatcher(IntentCatcher):
    def __init__(self, normal_sentence: dict):
        super().__init__()
        self.normal_sentence = normal_sentence

    def catch(self):
        intents = _read_json()

        for key, user_sentences in intents.items():
            # FIXME
            for user_sent in user_sentences:
                if user_sent in list(self.normal_sentence.values()):
                    return key
