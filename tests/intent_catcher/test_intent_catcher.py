import pytest

from answer_catcher.answer_catcher import AnswerCatcher
from intent_catcher.intent_catcher_with_cos_sim import IntentCatcher
from morph_tagging.builder import EmbedderBuilder
from morph_tagging.tagger import Tools


def generate_result(user_sentence):
    builder = EmbedderBuilder("tiny-bert2")
    emb = builder.build()
    catcher = IntentCatcher(user_sentence, emb)
    result = catcher.get_intent()
    print(result)
    return AnswerCatcher().catch_answer(result)


@pytest.mark.parametrize("user_sentence", ["привет",
                                           "здарова",
                                           "какие твои услуги",
                                           "В чем ваше преимущество",
                                           "Расскажи о команде",
                                           "Че по цене?"
                                           ])
def test_intent_catcher_positive_res(user_sentence):
    result = generate_result(user_sentence)
    print(result)
    assert result != "default"


@pytest.mark.parametrize("user_sentence", ["Извините я вас не понимаю",
                                           "как дела",
                                           "вау вот это да"])
def test_intent_catcher_negative_res(user_sentence):
    result = generate_result(user_sentence)
    print(result)
    with pytest.raises(AssertionError):
        assert result != "default"
