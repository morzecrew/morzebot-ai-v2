import pytest

from nltk.translate.bleu_score import sentence_bleu
from chit_chat.t5_ru.t5_ru import T5ChitChat


@pytest.mark.parametrize("user_sentence", ["привет! Ты кто?",
                                           "Какие твои любимые книги?",
                                           "Как тебя зовут?",
                                           "Что ты делаешь?",
                                           "Здравствуйте я Егор"
                                           ])
def test_chit_chat(user_sentence):
    test = T5ChitChat().response(user_sentence)
    print(test)
    score = sentence_bleu([user_sentence], test)
    print(score)
    assert score > 0.08
