import pytest

from chit_chat.t5_ru.t5_ru import T5ChitChat



@pytest.mark.parametrize("user_sentence", ["привет! Ты кто?",
                                           "Какие твои любимые книги?",
                                           "Как тебя зовут?",
                                           "Что ты делаешь?",
                                           "Здравствуйте я Егор"
                                           ])
def test_chit_chat(user_sentence):
    result = T5ChitChat().response(user_sentence)
    print(result)
    assert result != ""
