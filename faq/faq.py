from lib.preprocessing import Preprocessing
from lib.similarity import Evaluation
from morph_tagging.sent_cleaner import SentenceCleaner
from faq.csv_worker import TableWorker
import numpy as np


class FAQAnswerer:
    def __init__(self, uuid: str, model, treshold=0.4):
        self.emb = Preprocessing(model)
        self.threshold = treshold
        self.uuid = uuid
        # pass

    def answer(self, cleaned_question):
        faq_data = TableWorker(self.uuid).table
        if self.emb:
            pass
        else:
            return None

        faq_sentences = faq_data['Question']

        cleaned_sentences = SentenceCleaner().clean_sentence(faq_sentences, lower=True, stopwords=True)

        sent_embeddings = self.emb.preprocessing(cleaned_sentences)
        question_embedding = self.emb.preprocessing(cleaned_question)

        # Compute cos
        max_sim = -1
        index_sim = -1

        for index, faq_embedding in enumerate(sent_embeddings):
            sim = Evaluation().cos_dist(faq_embedding, question_embedding)
            if sim > max_sim:
                max_sim = sim
                index_sim = index

        if max_sim >= self.threshold:
            # FAQ_data.iloc[index_sim, 0]
            return faq_data.iloc[index_sim, 1]
        else:
            return None
