from intent_catcher.get_intents import GetIntentsEmb
from lib.emb.preprocessing import Preprocessing
import sys

from lib.sklearn.svm import SVM
from morph_tagging.builder import EmbedderBuilder
builder = EmbedderBuilder("tiny-bert2")
emb = builder.build()
class Trainer:
    def __init__(self, emb: Preprocessing):
        self.emb = emb
        self.user_intents = GetIntentsEmb(emb)
        pass

    def __enum_label(self, labels, label):
        return  labels.index(label)
    def __construct_training_data(self):
        input = []
        label = []
        keys = list(self.user_intents.get_intent_emb().keys())
        for k in keys:
            for v in self.user_intents.get_intent_emb()[k]:
                input.append(v)
                label.append(self.__enum_label(keys,k))

        return input, label
    def train(self,model_key):
        input, label = self.__construct_training_data()
        if model_key == 'svm':
            SVM().train(input,label)
        # if key == 'multiclass':
        # if key == 'multiclass_dropout':
        # if key == 'fnn':
        #
        # if key == 'logreg':






if __name__ == "__main__":
    Trainer(emb=emb).train('svm')