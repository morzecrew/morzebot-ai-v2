from intent_catcher.intent_catcher import NatashaCatcher, IntentCatcher
from morph_tagging.builder import MorphBuilder, Builder
from morph_tagging.tagger import Tools, DocParser


def intent_catcher_test():
    tools = Tools()
    sentence = "аренда дом"
    builder: Builder = MorphBuilder(tools=tools)
    normal_sentence = builder.build(sentence=sentence)

    catcher: IntentCatcher = NatashaCatcher(normal_sentence)
    response = catcher.catch()

    assert response is not None


intent_catcher_test()
