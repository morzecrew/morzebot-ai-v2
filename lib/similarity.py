import numpy as np
from numpy.linalg import norm


class CosinSimilarity:

    def __init__(self):
        pass

    def cos_sim(self, user_sent_emb, user_intent_emb):
        # user_sent_emb = np.array(user_sent_emb).reshape(1, -1)
        # user_intent_emb = np.array(user_intent_emb).reshape(1,-1)
        cosin = np.dot(user_sent_emb, user_intent_emb) / (norm(user_sent_emb, ord=2) * norm(user_intent_emb, ord=2))
        # cosin = cosine_similarity(user_sent_emb, user_intent_emb)
        return cosin
