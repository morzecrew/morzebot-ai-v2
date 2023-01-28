import pytest

from answer_catcher.answer_catcher import AnswerCatcher
from intent_catcher.intent_catcher_with_ml import IntentCatcherML
from intent_catcher.intent_catcher_with_cos_sim import IntentCatcherCos
from morph_tagging.builder import EmbedderBuilder
from lib.sklearn.svm import SVM
from lib.torch_models.torch_fnn import NeuralNetwork
from lib.torch_models.torch_multi_classifier import MultiClassClassifier
from morph_tagging.tagger import Tools


def generate_result(user_sentence):
    builder = EmbedderBuilder("tiny-bert2")
    emb = builder.build()
    # model = SVM(kernel='rbf')
    # model = NeuralNetwork()
    model = MultiClassClassifier()
    print('setup model')
    # model.load(filename='svm_model')
    # model.load(filename= 'fnn_model')
    model.load(filename='multiclass_classification_model')
    print('load model')
    catcher = IntentCatcherCos(user_sentence, emb, model=model)
    catcher = IntentCatcherML(user_sentence, emb,model=model)
    result = catcher.get_intent()
    print(result)
    return AnswerCatcher().catch_answer(result)


@pytest.mark.parametrize("user_sentence", ["привет",
                                           "хочу забронировать баню",
                                           "у вас такая крутая база отдыха хочу забронировать у васс дом"
                                           ])
def test_intent_catcher_positive_res(user_sentence):
    result = generate_result(user_sentence)
    print(result)
    assert result != "Извините, я вас не понимаю"


@pytest.mark.parametrize("user_sentence", ["привет ты кто",
                                           "как дела",
                                           "вау вот это да"])
def test_intent_catcher_negative_res(user_sentence):
    result = generate_result(user_sentence)
    with pytest.raises(AssertionError):
        assert result != "Извините, я вас не понимаю"
