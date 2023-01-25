import pytest

from answer_catcher.answer_catcher import AnswerCatcher
from intent_catcher.intent_catcher import NatashaCatcher, IntentCatcher
from morph_tagging.builder import MorphBuilder, Builder
from morph_tagging.tagger import Tools, DocParser



def generate_result(sentence):
    tools = Tools()
    builder: Builder = MorphBuilder(tools=tools)
    normal_sentence = builder.build(sentence=sentence, uuid=None)
    catcher: IntentCatcher = NatashaCatcher(normal_sentence)
    response = catcher.catch()
    variable: IdCatcher = VariableCatcher(response, normal_sentence)
    var = variable.get_variable()
    return var


@pytest.mark.parametrize("user_sentence", ["фыв привет бронь бани",
                                           "хочу забронировать баню",
                                           "у вас такая крутая база отдыха хочу забронировать баню",
                                           "забронировать баню на 20 часов",
                                           "хочу забронировать баню на завтра",
                                           "хочу забронировать баню на завтра на вечер",
                                           "бронь бани"
                                           ])
def test_var_catcher_pos_res(user_sentence):
    booking_synonym = 'бронь'
    var = generate_result(user_sentence)
    if booking_synonym not in var['payload'].keys():
        booking_synonym = 'забронировать'
    assert var['payload'][booking_synonym]['values']['level_1'] == "баня"
