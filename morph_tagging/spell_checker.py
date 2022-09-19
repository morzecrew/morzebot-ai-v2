import jamspell

from morph_tagging import layout_swapper

spell = jamspell.TSpellCorrector()
# https://drive.google.com/open?id=11Qko7W4FVHdcXnKE1G45PsY1df34GwgM
spell.LoadLangModel('../morph_tagging/jamspell_ru_model_subtitles.bin')


class SpellCorrector:
    def __init__(self):
        pass

    def correct(self, sentence: str):
        return ' '.join([spell.FixFragment(layout_swapper.swap_engrus(word)) for word in sentence.split()])
