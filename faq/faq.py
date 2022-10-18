import os
from navec import Navec
from sklearn.metrics.pairwise import cosine_similarity;

from faq.embedding import getPhraseEmbedding
from faq.csv_worker import TableWorker

# Load dataset and examine dataset, rename columns to questions and answers
DATA_PATH = os.path.join(os.path.dirname(os.getcwd()),os.path.join("data", "hudlit_12B_500K_300d_100q.tar"))

try:
    navec = Navec.load(DATA_PATH)
except:
    navec = None



class FAQAnswerer:
    def __init__(self, model = navec):
        self.model = model
        # pass



    def answer(self, question, FAQ_data=TableWorker().table):
        if self.model:
            pass
        else:
            return None
        max_sim = -1;
        index_sim = -1;
        sent_embeddings = [];
        ##FIXME: add stop words and garbage words deleter
        cleaned_sentences = FAQ_data['Question']
        ##

        for sent in cleaned_sentences:
            sent_embeddings.append(self.__sent_embedding(sent))
        question_embedding = self.__sent_embedding(question)
        for index, faq_embedding in enumerate(sent_embeddings):
            # sim=cosine_similarity(embedding.reshape(1, -1),question_embedding.reshape(1, -1))[0][0];
            sim = cosine_similarity(faq_embedding, question_embedding)[0][0];
            # print(index, sim, sentences[index])
            if sim > max_sim:
                max_sim = sim;
                index_sim = index;
        print(FAQ_data.iloc[index_sim, 0])
        return FAQ_data.iloc[index_sim, 1]

    def __sent_embedding(self, sent):
        return getPhraseEmbedding(sent, self.model)
