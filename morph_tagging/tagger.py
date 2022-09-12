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


class Tagger:
    def __init__(self):
        pass


class Tools:
    def __init__(self, segmenter, morph_vocab, emb):
        self.segmenter = segmenter
        self.morph_vocab = morph_vocab
        self.emb = emb

        self.morph_tagger = NewsMorphTagger(emb)
        self.syntax_parser = NewsSyntaxParser(emb)
        self.ner_tagger = NewsNERTagger(emb)


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
    def __init__(self, tools: Tools, doc_parser: DocParser):
        self.doc_parser = doc_parser
        self.tools = tools

    def normalize(self):
        doc = self.doc_parser.doc
        for token in doc.tokens:
            token.lemmatize(self.tools.morph_vocab)
        # for span in doc.spans:
        #     span.normalize(self.tools.morph_vocab)
        # TODO: RESPONSE
        return {_.text: _.lemma for _ in doc.tokens}
