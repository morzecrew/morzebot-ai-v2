import os
import jamspell
from spellchecker_wrapper import SpellSheckerWrapper

jam_spell = jamspell.TSpellCorrector()
# https://drive.google.com/drive/folders/1tl-UoXosujSVJRNKcr99xyUuNfGfcrMe
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())),
                         os.path.join("data", "jamspell_ru_model_subtitles.bin"))

jam_spell.LoadLangModel(DATA_PATH)


class JamSpellWarapper(SpellSheckerWrapper):
    def __init__(self, model=jam_spell):
        super().__init__(model)

    def correct(self, sentence):
        return self.model.FixFragment(sentence)
