from spellchecker import SpellChecker

spell = SpellChecker(language='ru')


# TODO: add in exceptions "морзе", because spellchecker corrects it into "море"

class SpellCorrector:
    def __init__(self):
        pass

    # FIXME: find new library for correcting text
    def correct(self, sentence: str):
        return ' '.join([spell.correction(word) for word in sentence.split()])
