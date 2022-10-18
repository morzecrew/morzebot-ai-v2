import numpy


def getWordVec(word, model):
    samp = model['навек'];
    vec = [0] * len(samp);
    try:
        vec = model[word];
    except:
        vec = [0] * len(samp);
    return (vec)


def getPhraseEmbedding(phrase, embeddingmodel):
    samp = getWordVec('навек', embeddingmodel);
    vec = numpy.array([0] * len(samp));
    den = 0;
    for word in phrase.split():
        # print(word)
        den = den + 1;
        vec = vec + numpy.array(getWordVec(word, embeddingmodel));
    # vec=vec/den;
    # return (vec.tolist());
    return vec.reshape(1, -1)
