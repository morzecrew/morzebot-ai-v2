import pytest

from answer_catcher.answer_catcher import AnswerCatcher
from catchers.intent_catcher_with_cos_dist import IntentCatcher
from lib.preprocessing import Preprocessing
from morph_tagging.builder import MorphBuilder, Builder
#from morph_tagging.spell_checker import SpellCorrector
from morph_tagging.tagger import Tools, DocParser
from variable_case.variable_reserve import ReserveCatcher, VariableCatcher


def generate_result(user_sentence):
    tools = Tools()
    builder: Builder = MorphBuilder(tools=tools)
    normal_sentence = builder.build(sentence=user_sentence)
    #print("normal", normal_sentence)
    emb = Preprocessing(model_emb=tools.emb)
    catcher = IntentCatcher(user_sentence, emb)
    intent_response = catcher.get_intent()
    print(intent_response)
    reserve = ReserveCatcher(intent_response, normal_sentence).get_variable()
    print(reserve)
    return AnswerCatcher().catch_answer(intent_response)


@pytest.mark.parametrize("user_sentence", ["привет дом",
                                           "хуй]",
                                           "забронировать первый и второй дом"
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


