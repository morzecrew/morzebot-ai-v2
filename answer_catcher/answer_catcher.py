import json
import os

from data.path_to_data import get_data_path

DATA_PATH = os.path.join(get_data_path(), "user_answers.json")


def _read_json():
    file = open(DATA_PATH, encoding='UTF-8')
    return json.loads(file.read())


class AnswerCatcher:
    def catch_answer(self, intent):
        user_answers = _read_json()

        if intent is None:
            return user_answers["default"]

        for key, value in user_answers.items():
            if key == intent["key"]:
                return value

        return user_answers["default"]
