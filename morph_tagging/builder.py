from typing import Union
#from morph_tagging.spell_checker import SpellCorrector
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

    def build(self, sentence, *args):
        # if uuid is not None:
        #     if Settings(uuid).is_speller_enabled():
        #         corrected_text = SpellCorrector().correct(sentence)
        #     else:
        #         corrected_text = sentence
        # else:
        #     corrected_text = SpellCorrector().correct(sentence)

        doc_parser = DocParser(self.tools, sentence)
        normalized_intent = Normalizer(self.tools).normalize(doc_parser)
        return normalized_intent
