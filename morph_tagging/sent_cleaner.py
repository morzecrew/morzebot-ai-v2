import re

# https://regex101.com/
regular_expression = r'[^(ёа-яА-Я0-9 )]+|(\b[^(ивксояИВКСОЯ)]{1}\b )'

DATA_PATH = "./data/stopwords_russian.txt"
stopwords_file = open(DATA_PATH, "r")
data = stopwords_file.read()
data_list = data.split("\n")
# print(data_into_list)
stopwords_file.close()


class SentenceCleaner:
    def __init__(self):
        pass

    def clean_sentence(self, text, lower=True, stopwords=True):

        if isinstance(text, str):
            if lower:
                text = text.lower().strip()
            if stopwords:

                return ' '.join([w for w in re.sub(
                    regular_expression, '',
                    text).split() if w not in data_list])
            else:
                return re.sub(regular_expression, '', text)

        else:
            if lower:
                [sent.lower().strip() for sent in text]
            if stopwords:
                return [' '.join([w for w in re.sub(
                    regular_expression, '',
                    sent).split() if w not in data_list]) for sent in text]
            else:
                return [re.sub(regular_expression, '', sent) for sent in text]
