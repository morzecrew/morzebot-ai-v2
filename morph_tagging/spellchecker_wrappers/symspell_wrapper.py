import os
from symspellpy import SymSpell
from spellchecker_wrapper import SpellSheckerWrapper

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), os.path.join("data", "ru-100k.txt"))

sym_spell = SymSpell()
sym_spell.load_dictionary(DATA_PATH, 0, 1, encoding="UTF-8")


# # max edit distance per lookup (per single word, not per whole input string)
# suggestions = sym_spell.lookup_compound(input_term, max_edit_distance=2, transfer_casing=True)
# # display suggestion term, edit distance, and term frequency
# for suggestion in suggestions:
#     print(suggestions[0].term)
#     print('\n')

class SymSpellWarapper(SpellSheckerWrapper):
    def __init__(self, model=sym_spell):
        super().__init__(model)

    def correct(self, sentence):
        return self.model.lookup_compound(sentence, max_edit_distance=2, transfer_casing=True)[0].term
