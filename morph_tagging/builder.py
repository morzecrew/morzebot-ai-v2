from typing import Union
from morph_tagging.spell_checker import SpellCorrector
from morph_tagging.sent_cleaner import SentenceCleaner
from morph_tagging.tagger import Normalizer, DocParser, Extractor, Tools
from tools.settings import Settings


class Builder:
    def __init__(self, tools: Tools):
        self.tools = tools

    def build(self, sentence, uuid):
        raise NotImplementedError


class MorphBuilder(Builder):
    def __init__(self, tools: Tools):
        super().__init__(tools)

    def build(self, sentence, uuid):
        cleaned_text = SentenceCleaner().clean_sentence(sentence, lower=True, stopwords=True)
        if uuid is not None:
            if Settings(uuid).is_speller_enabled():
                corrected_text = SpellCorrector().correct(cleaned_text)
                doc_parser = DocParser(self.tools, corrected_text)
            else:
                doc_parser = DocParser(self.tools, cleaned_text)
        else:
            corrected_text = cleaned_text
            doc_parser = DocParser(self.tools, corrected_text)

        normalized_intent = Normalizer(self.tools).normalize(doc_parser)
        return normalized_intent
