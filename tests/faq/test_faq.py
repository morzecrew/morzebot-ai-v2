import pytest

from faq.faq import FAQAnswerer
from morph_tagging.sent_cleaner import SentenceCleaner
from morph_tagging.tagger import Tools


def generate_result(user_sentence, uuid):
    tools = Tools()
    cleaned_text = SentenceCleaner().clean_sentence(user_sentence)
    return FAQAnswerer(uuid, tools.emb).answer(cleaned_text)


@pytest.mark.parametrize("user_sentence, uuid", [("Где взять код регистрации?", "1")])
def test_intent_catcher_positive_res(user_sentence, uuid):
    result = generate_result(user_sentence, uuid)
    assert result != None
