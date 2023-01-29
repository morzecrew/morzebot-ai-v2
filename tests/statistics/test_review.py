import pytest

from statistics.review import Reviewer
from dotenv import load_dotenv
load_dotenv()





@pytest.mark.parametrize("user_sentence", ["Мне не нравится ваш товар",
                                           "Этот платиковый круг оказался полным говном",
                                           "Крутой продукт однозначно рекомендую",
                                           "Товар огонь!!!",
                                           "Нормас, на три",
                                           "Если честно, товар так себе"
                                           ])

def generate_result(user_sentence):
    reviewer = Reviewer()
    result = reviewer.get_sentiment(user_sentence)
    print(result)
    return result