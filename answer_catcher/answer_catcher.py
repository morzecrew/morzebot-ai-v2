import json
import os

DATA_PATH = os.getcwd() + "\\data\\user_answers.json"


def _read_json():
    file = open(DATA_PATH, encoding='UTF-8')
    return json.loads(file.read())


class AnswerCatcher:
    def catch_answer(self, intent):
        user_answers = _read_json()

        for key, value in user_answers.items():
            if key == intent:
                return value

        return user_answers["default"]
