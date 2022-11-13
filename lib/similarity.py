import numpy as np
from numpy.linalg import norm


class Evaluation:
    def __init__(self):
        pass

    def cos_dist(self, user_sent_emb, user_intent_emb):
        cosin = np.dot(user_sent_emb, user_intent_emb) / (norm(user_sent_emb, ord=2) * norm(user_intent_emb, ord=2))
        # cosin = cosine_similarity(user_sent_emb, user_intent_emb)
        return cosin

    def pirson(user_sent_emb, user_intent_emb):
        sum_emb = np.sum(user_sent_emb, axis=0)
        sum_intent_emb = np.sum(user_intent_emb, axis=0)
        average_emb = sum_emb / np.size(user_sent_emb, 1)
        average_test_emb = sum_intent_emb / np.size(user_intent_emb, 1)
        sum_multiply = 0
        sum_emb_square = 0
        sum_intent_emb_square = 0
        for iter in range(np.size(user_sent_emb, 1)):
            diff_emb = user_sent_emb[0][iter] - sum_emb
            diff_intent_emb = user_intent_emb[0][iter] - sum_intent_emb

            multiply = diff_emb * diff_intent_emb
            sum_multiply += multiply

            sum_emb_square += np.square(diff_emb)
            sum_intent_emb_square += np.square(diff_intent_emb)

        return sum_multiply / np.sqrt(sum_emb_square * sum_intent_emb_square)

    def euc(user_sent_emb, user_intent_emb):
        sum_diff_square = 0
        for iter in range(np.size(user_sent_emb, 1)):
            diff_emb = user_sent_emb[0][iter] - user_intent_emb[0][iter]
            sum_diff_square += np.square(diff_emb)

        return np.sqrt(sum_diff_square)

    def sigma_emb(user_emb):
        # for one vector?
        sum_emb = np.sum(user_emb, axis=0)
        sum_diff_square = 0
        for iter in range(np.size(user_emb, 1)):
            diff_emb = user_emb[0][iter] - sum_emb
            sum_diff_square += np.square(diff_emb)

        return np.sqrt(sum_diff_square / np.size(user_emb, 1))

    def sigma_two_emb(user_sent_emb, user_intent_emb):
        # deviation of user emb from intent emb
        sum_intent_emb = np.sum(user_intent_emb, axis=0)
        sum_diff_square = 0
        for iter in range(np.size(user_sent_emb, 1)):
            diff_emb = user_sent_emb[0][iter] - sum_intent_emb
            sum_diff_square += np.square(diff_emb)

        return np.sqrt(sum_diff_square / np.size(user_sent_emb, 1))

    def gauss(user_sent_emb, user_intent_emb):

        # TODO sigma one or sigma two?
        return np.exp(-np.square(euc(user_sent_emb, user_intent_emb)) / (2 * sigma_emb(user_sent_emb)))