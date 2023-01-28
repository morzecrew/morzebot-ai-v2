from intent_catcher.get_intents import GetIntentsEmb
from lib.emb.preprocessing import Preprocessing
import numpy as np
import sys

from lib.sklearn.svm import SVM
from torch_models.torch_fnn import NeuralNetwork
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
        if model_key == 'multiclass':
            MultiClassClassifier(input_size=len(input[0]),hidden_size=60,
                                 output_size=len(list(self.user_intents.get_intent_emb().keys()))).train(np.array(input),np.array(label))

        # if model_key == 'multiclass_dropout':
        if model_key == 'fnn':
            NeuralNetwork(input_size=len(input[0]), hidden_size=60,
                                    output_size=len(list(self.user_intents.get_intent_emb().keys()))).train(
                np.array(input), np.array(label))

        # if model_key == 'logreg':






if __name__ == "__main__":
    Trainer(emb=emb).train('multiclass')