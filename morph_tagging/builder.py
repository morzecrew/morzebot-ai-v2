from typing import Union

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
        doc_parser = DocParser(self.tools, sentence)

        return Normalizer(self.tools).normalize(doc_parser)