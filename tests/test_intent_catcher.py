import pytest

from answer_catcher.answer_catcher import AnswerCatcher
from intent_catcher.intent_catcher import NatashaCatcher, IntentCatcher
from morph_tagging.builder import MorphBuilder, Builder
from morph_tagging.spell_checker import SpellCorrector
from morph_tagging.tagger import Tools, DocParser


@pytest.mark.parametrize("user_sentence", ["фыв привет бронь дом",
                                           "хочу забронировать баню",
                                           "у вас такая крутая база отдыха хочу забронировать у васс дом"])
def test_intent_catcher_positive_res(user_sentence):
    tools = Tools()
    builder: Builder = MorphBuilder(tools=tools)
    normal_sentence = builder.build(sentence=user_sentence)
    catcher: IntentCatcher = NatashaCatcher(normal_sentence)
    response = catcher.catch()
    result = AnswerCatcher().catch_answer(response)

    assert result != "Извините, я вас не понимаю"


@pytest.mark.parametrize("user_sentence", ["привет ты кто",
                                           "как дела",
                                           "вау вот это да"])
def test_intent_catcher_negative_res(user_sentence):
    tools = Tools()
    builder: Builder = MorphBuilder(tools=tools)
    normal_sentence = builder.build(sentence=user_sentence)
    catcher: IntentCatcher = NatashaCatcher(normal_sentence)
    response = catcher.catch()
    result = AnswerCatcher().catch_answer(response)
    with pytest.raises(AssertionError):
        assert result != "Извините, я вас не понимаю"