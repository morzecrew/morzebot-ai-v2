import json
import os

from natasha import Doc


class IntentCatcher:
    def __init__(self):
        pass

    def catch(self):
        raise NotImplementedError


DATA_PATH = os.path.join(os.getcwd(), os.path.join("data", "user_intents.json"))


def _read_json():
    file = open(DATA_PATH, encoding='UTF-8')
    return json.loads(file.read())


class NatashaCatcher(IntentCatcher):
    def __init__(self, normal_sentence: Doc):
        super().__init__()
        self.normal_sentence = normal_sentence

    def catch(self):
        intents = _read_json()
        for key, user_sentences in intents.items():
            # FIXME
            for user_sent in user_sentences:
                for token in self.normal_sentence.tokens:
                    if user_sent == token.lemma:
                        return {"key": key, "user_sent": user_sent, "token_id": token.id}

        return None
