import pytest

from answer_catcher.answer_catcher import AnswerCatcher
from intent_catcher.intent_catcher import NatashaCatcher, IntentCatcher
from morph_tagging.builder import MorphBuilder, Builder
from morph_tagging.tagger import Tools


def generate_result(user_sentence):
    tools = Tools()
    builder: Builder = MorphBuilder(tools=tools)
    normal_sentence = builder.build(sentence=user_sentence, uuid=None)
    catcher: IntentCatcher = NatashaCatcher(normal_sentence)
    response = catcher.catch()
    return AnswerCatcher().catch_answer(response)


@pytest.mark.parametrize("user_sentence", ["фыв привет бронь дом",
                                           "хочу забронировать баню",
                                           "у вас такая крутая база отдыха хочу забронировать у васс дом"
                                           ])
def test_intent_catcher_positive_res(user_sentence):
    result = generate_result(user_sentence)
    assert result != "Извините, я вас не понимаю"


@pytest.mark.parametrize("user_sentence", ["привет ты кто",
                                           "как дела",
                                           "вау вот это да"])
def test_intent_catcher_negative_res(user_sentence):
    result = generate_result(user_sentence)
    with pytest.raises(AssertionError):
        assert result != "Извините, я вас не понимаю"