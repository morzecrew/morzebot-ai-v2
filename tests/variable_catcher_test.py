from answer_catcher.answer_catcher import AnswerCatcher
from intent_catcher.intent_catcher import NatashaCatcher, IntentCatcher
from morph_tagging.builder import MorphBuilder, Builder
from morph_tagging.tagger import Tools, DocParser
from intent_catcher.variable_catcher import IdCatcher,VariableCatcher


def intent_catcher_test():
    tools = Tools()
    sentence = "забронировать третий дом"
    builder: Builder = MorphBuilder(tools=tools)
    normal_sentence = builder.build(sentence=sentence)
    catcher: IntentCatcher = NatashaCatcher(normal_sentence)
    response = catcher.catch()
    print(response)
    variable:IdCatcher = VariableCatcher(response, normal_sentence)
    var = variable.get_variable()
    print(var)

    result = AnswerCatcher().catch_answer(response)

    print(result)
    assert result != "Извините, я вас не понимаю"


intent_catcher_test()
