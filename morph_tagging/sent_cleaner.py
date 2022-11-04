import re
from nltk.corpus import stopwords

DATA = set(stopwords.words('russian'))
# https://regex101.com/
regular_expression = r'[^(ёа-яА-Я0-9 )]+|(\b[^(ивксояИВКСОЯ)]{1}\b )'


class SentenceCleaner:
    def __init__(self):
        pass

    def clean_sentence(self, sentence: str, lower=True, stopwords=True):
        if lower:
            sentence = sentence.lower().strip()
        if stopwords:

            return ' '.join([w for w in re.sub(
                regular_expression, '',
                sentence).split() if w not in DATA])
        else:
            return re.sub(regular_expression, '', sentence)
