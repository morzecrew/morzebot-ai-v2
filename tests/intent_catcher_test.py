from answer_catcher.answer_catcher import AnswerCatcher
from intent_catcher.intent_catcher import NatashaCatcher, IntentCatcher
from morph_tagging.builder import MorphBuilder, Builder
from morph_tagging.tagger import Tools, DocParser


def intent_catcher_test():
    tools = Tools()
    sentence = "првет мурзе, hjym дом"
    builder: Builder = MorphBuilder(tools=tools)
    normal_sentence = builder.build(sentence=sentence)
    catcher: IntentCatcher = NatashaCatcher(normal_sentence)
    response = catcher.catch()
    result = AnswerCatcher().catch_answer(response)

    print(result)
    assert result != "првет морзе, бронь дом"
    assert result != "Извините, я вас не понимаю"


intent_catcher_test()
