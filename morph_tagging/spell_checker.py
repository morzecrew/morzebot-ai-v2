import jamspell

# from morph_tagging.layout_swapper import LayoutSwapper

spell = jamspell.TSpellCorrector()
# https://drive.google.com/drive/folders/1tl-UoXosujSVJRNKcr99xyUuNfGfcrMe
print(spell.LoadLangModel("morph_tagging/jamspell_ru_model_subtitles.bin"))


class SpellCorrector:
    def __init__(self):
        pass

    # def correct(self, sentence: str):
        # return ' '.join([spell.FixFragment(LayoutSwapper().swap_engrus(word)) for word in sentence.split()])
