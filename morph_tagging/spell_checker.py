from spellchecker_wrappers.spellchecker_wrapper import SpellSheckerWrapper
from morph_tagging.layout_swapper import LayoutSwapper



class SpellCorrector:
    def __init__(self, wrapper: SpellSheckerWrapper):
        self.wrapper = wrapper

    def correct(self, sentence: str):
        # at first change layout, after that correct all text
        return self.wrapper.correct(' '.join([LayoutSwapper().swap_engrus(word) for word in sentence.split()]))
