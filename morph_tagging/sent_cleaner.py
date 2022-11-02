import re
from nltk.corpus import stopwords

DATA = set(stopwords.words('russian'))
# https://regex101.com/
regular_expression = r'(\w+:\/\/\S+)|(@\[А-Яа-яёЁ0-9])|(\b[^(ивксояИВКСОЯ)]{1}\b )|([^0-9А-Яа-яёЁ[^-] \t])|^rt|http.+?'


class SentenceCleaner:
    def __init__(self):
        pass

    def clean_sentence(self, sentence: str, lower=True, stopwords=False):
        if lower:
            sentence = sentence.lower().strip()
        if stopwords:
            # (\w+:\/\/\S+)|(@\[А-Яа-яёЁ0-9])|(\b[^(ивксояИВКСОЯ)]{1}\b )|([^0-9А-Яа-яёЁ \t])|^rt|http.+?
            return ' '.join([w for w in re.sub(
                regular_expression, '',
                sentence).split() if w not in DATA])
        else:
            return re.sub(regular_expression, '', sentence)
