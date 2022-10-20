import pytest

from answer_catcher.answer_catcher import AnswerCatcher
from intent_catcher.intent_catcher import NatashaCatcher, IntentCatcher
from intent_catcher.variable_catcher import VariableCatcher, IdCatcher
from morph_tagging.builder import MorphBuilder, Builder
#from morph_tagging.spell_checker import SpellCorrector
from morph_tagging.tagger import Tools, DocParser


def generate_result(user_sentence):
    tools = Tools()
    builder: Builder = MorphBuilder(tools=tools)
    normal_sentence = builder.build(sentence=user_sentence)
    catcher: IntentCatcher = NatashaCatcher(normal_sentence)
    intent_response = catcher.catch()
    variable: IdCatcher = VariableCatcher(intent_response, normal_sentence)
    response = variable.get_variable()
    print(response)
    return AnswerCatcher().catch_answer(response)


@pytest.mark.parametrize("user_sentence", ["фыв привет бронировать дом",
                                           "хочу забронировать баню",
                                           "у вас такая крутая база отдыха хочу забронировать дом"
                                           ])
def test_intent_catcher_positive_res(user_sentence):
    result = generate_result(user_sentence)
    print(result)
    assert result != "Извините, я вас не понимаю"


@pytest.mark.parametrize("user_sentence", ["привет ты кто",
                                           "как дела",
                                           "вау вот это да"])
def test_intent_catcher_negative_res(user_sentence):
    result = generate_result(user_sentence)
    with pytest.raises(AssertionError):
        assert result != "Извините, я вас не понимаю"


