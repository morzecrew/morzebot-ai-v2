from typing import Union
from morph_tagging.spell_checker import SpellCorrector
from spellchecker_wrappers.symspell_wrapper import SymSpellWarapper
from morph_tagging.tagger import Normalizer, DocParser, Extractor, Tools


class Builder:
    def __init__(self, tools: Tools):
        self.tools = tools

    def build(self, sentence):
        raise NotImplementedError


class MorphBuilder(Builder):
    def __init__(self, tools: Tools):
        super().__init__(tools)

    def build(self, sentence):
        corrected_text = SpellCorrector(SymSpellWarapper()).correct(sentence)
        # doc_parser = DocParser(self.tools, sentence)
        doc_parser = DocParser(self.tools, corrected_text)
        normalized_intent = Normalizer(self.tools).normalize(doc_parser)
        return normalized_intent
