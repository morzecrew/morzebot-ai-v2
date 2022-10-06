import jamspell
import os
from morph_tagging.layout_swapper import LayoutSwapper

spell = jamspell.TSpellCorrector()
# https://drive.google.com/drive/folders/1tl-UoXosujSVJRNKcr99xyUuNfGfcrMe
DATA_PATH = os.path.join(os.getcwd(),os.path.join("data","jamspell_ru_model_subtitles.bin"))
spell.LoadLangModel(DATA_PATH)



class SpellCorrector:
    def __init__(self):
        pass

    def correct(self, sentence: str):
        return ' '.join([spell.FixFragment(LayoutSwapper().swap_engrus(word)) for word in sentence.split()])
