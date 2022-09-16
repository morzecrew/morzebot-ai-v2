# from spellchecker import SpellChecker
#
# spell = SpellChecker(language='ru')
import jamspell

spell = jamspell.TSpellCorrector()
# https://drive.google.com/open?id=11Qko7W4FVHdcXnKE1G45PsY1df34GwgM
spell.LoadLangModel('../morph_tagging/jamspell_ru_model_subtitles.bin')


# TODO: add in exceptions "морзе", because spellchecker corrects it into "море"

class SpellCorrector:
    def __init__(self):
        pass

    # FIXME: find new library for correcting text
    def correct(self, sentence: str):
        return ' '.join([spell.FixFragment(word) for word in sentence.split()])
