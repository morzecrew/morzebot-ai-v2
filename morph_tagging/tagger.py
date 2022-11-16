from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor,

    Doc
)


class Tools:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __del__(self):
        Tools.__instance = None

    def __init__(self):
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()

        self.ner_tagger = NewsNERTagger(self.emb)
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.morph_tagger = NewsMorphTagger(self.emb)


class Extractor:
    def __init__(self, tools: Tools):
        self.names_extractor = NamesExtractor(tools.morph_vocab)
        self.dates_extractor = DatesExtractor(tools.morph_vocab)
        self.money_extractor = MoneyExtractor(tools.morph_vocab)
        self.addr_extractor = AddrExtractor(tools.morph_vocab)


class DocParser:
    def __init__(self, tools: Tools, text):
        self.doc = Doc(text)
        self.tools = tools

    def parse(self):
        self.doc.segment(self.tools.segmenter)
        self.doc.tag_morph(self.tools.morph_tagger)
        self.doc.parse_syntax(self.tools.syntax_parser)
        self.doc.tag_ner(self.tools.ner_tagger)

        return self.doc


class Normalizer:
    def __init__(self, tools: Tools):
        self.tools = tools

    def normalize(self, doc_parser: DocParser):
        doc = doc_parser.parse()

        doc = self.__lemmatize(doc)
        # self.__normalize(doc)

        # TODO: RESPONSE
        return doc

    def __lemmatize(self, doc):
        for token in doc.tokens:
            token.lemmatize(self.tools.morph_vocab)
        return doc

    def __normalize(self, doc):
        for span in doc.spans:
            span.normalize(self.tools.morph_vocab)
        return doc
