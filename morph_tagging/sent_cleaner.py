import re
from nltk.corpus import stopwords

DATA = set(stopwords.words('russian'))


class SentenceCleaner:
    def __init__(self):
        pass

    def clean_sentence(self, sentence: str, lower=True, stopwords=False):
        if lower:
            sentence = sentence.lower().strip()
        if stopwords:
            return ' '.join([w for w in re.sub(r'(.)(\/)\W*', '', sentence).split() if w not in DATA])
        else:
            return re.sub(r'(.)(\/)\W*', '', sentence)
