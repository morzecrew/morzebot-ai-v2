import numpy as np
from numpy.linalg import norm


class Evaluation():
    def __init__(self):
        pass

    def cos_dist(self, user_sent_emb, user_intent_emb):
        try:
            cosin = np.dot(user_sent_emb, user_intent_emb) / (norm(user_sent_emb, ord=2) * norm(user_intent_emb, ord=2))
        except:
            cosin = 0

        return cosin

    def pearson(self, user_sent_emb, user_intent_emb):
        sum_emb = np.sum(user_sent_emb)
        sum_intent_emb = np.sum(user_intent_emb)
        average_emb = sum_emb / np.size(user_sent_emb, 0)
        average_test_emb = sum_intent_emb / np.size(user_intent_emb, 0)
        sum_multiply = 0
        sum_emb_square = 0
        sum_intent_emb_square = 0
        for iter in range(np.size(user_sent_emb, 0)):
            diff_emb = user_sent_emb[iter] - sum_emb
            diff_intent_emb = user_intent_emb[iter] - sum_intent_emb

            multiply = diff_emb * diff_intent_emb
            sum_multiply += multiply

            sum_emb_square += np.square(diff_emb)
            sum_intent_emb_square += np.square(diff_intent_emb)

        return abs(sum_multiply / np.sqrt(sum_emb_square * sum_intent_emb_square))

    def pearson_uncentered(self, user_sent_emb, user_intent_emb):
        sum_emb = np.sum(user_sent_emb)
        sum_intent_emb = np.sum(user_intent_emb)
        average_emb = sum_emb / np.size(user_sent_emb, 0)
        average_test_emb = sum_intent_emb / np.size(user_intent_emb, 0)
        sum_multiply = 0
        sum_emb_multiply = 0
        sum_emb_square = 0
        sum_intent_emb_square = 0
        for iter in range(np.size(user_sent_emb, 0)):
            diff_emb = user_sent_emb[iter] - sum_emb
            diff_intent_emb = user_intent_emb[iter] - sum_intent_emb

            multiply = user_sent_emb[iter] * user_intent_emb[iter]
            sum_multiply += multiply

            sum_emb_square += np.square(diff_emb)
            sum_intent_emb_square += np.square(diff_intent_emb)

        return abs(sum_multiply / np.sqrt(sum_emb_square * sum_intent_emb_square))

    # preprocessing for spearmans correlation
    def spearmans_ranking(self, sent_emb):

        length = np.size(sent_emb, 0)
        # Rank Vector
        rank = [None for _ in range(length)]

        for i in range(length):
            r = 1
            s = 1
            # Count no of smaller elements
            # in 0 to i-1
            for j in range(i):
                if (sent_emb[j] < sent_emb[i]):
                    r += 1
                if (sent_emb[j] == sent_emb[i]):
                    s += 1
            # Count no of smaller elements
            # in i+1 to N-1
            for j in range(i + 1, length):
                if (sent_emb[j] < sent_emb[i]):
                    r += 1
                if (sent_emb[j] == sent_emb[i]):
                    s += 1
            # fractional_rank = r + (n-1)/2
            rank[i] = r + (s - 1) * 0.5

        return rank

    def spearmans(self, user_sent_emb, user_intent_emb):
        return self.pearson(self.spearmans_ranking(user_sent_emb), self.spearmans_ranking(user_intent_emb))

    def euc(self, user_sent_emb, user_intent_emb):
        return sum([(user_sent_emb[x] - user_intent_emb[x]) ** 2 for x in range(len(user_sent_emb))]) ** 0.5

    def manhattan(self, user_sent_emb, user_intent_emb):
        return sum(abs(value1 - value2) for value1, value2 in zip(user_sent_emb, user_intent_emb))

    def sigma_two_emb(self, user_sent_emb, user_intent_emb):
        # deviation of user emb from intent emb
        sum_intent_emb = np.sum(user_intent_emb, axis=0)
        sum_diff_square = 0
        for iter in range(np.size(user_sent_emb, 0)):
            diff_emb = user_sent_emb[iter] - sum_intent_emb
            sum_diff_square += np.square(diff_emb)

        return np.sqrt(sum_diff_square / np.size(user_sent_emb, 0))

    def gauss(self, user_sent_emb, user_intent_emb):
        return np.exp(-np.square(self.euc(user_sent_emb, user_intent_emb)) / (
                2 * np.square(self.sigma_two_emb(user_sent_emb, user_intent_emb))))

    def euc_normalized(self, user_sent_emb, user_intent_emb):
        return sum([((user_sent_emb[x] - user_intent_emb[x]) ** 2) / np.size(user_sent_emb, 0) for x in
                    range(len(user_sent_emb))]) ** 0.5

    def cov(self, x, y):
        X = np.array([x, y])
        X = X - X.mean(axis=0)
        h, w = X.shape
        return X.T @ X / (h - 1)

    def mahalanobis(self, user_sent_emb, user_intent_emb):
        cov = self.cov(user_sent_emb, user_intent_emb)
        if np.linalg.det(cov) != 0:
            inv_covmat = np.linalg.inv(cov)
            emb_diff = user_sent_emb - user_intent_emb
            emb_diff_t = np.transpose([emb_diff])
            product = np.dot(np.dot(emb_diff, inv_covmat), emb_diff_t)
            return np.sqrt(product)
        else:
            return 0

    # solve det = 0 problem
    def euc_mahalanobis(self, user_sent_emb, user_intent_emb):
        cov = self.cov(user_sent_emb, user_intent_emb)
        if np.linalg.det(cov + np.identity(cov.shape[0])) != 0:
            inv_covmat = np.linalg.inv(cov + np.identity(cov.shape[0]))
            emb_diff = np.subtract(user_sent_emb, user_intent_emb)
            emb_diff_t = np.transpose([emb_diff])
            product = np.dot(np.dot(emb_diff, inv_covmat), emb_diff_t)
            return np.sqrt(product)
        else:
            return 0

    def chebychev(self, user_sent_emb, user_intent_emb):
        return max([np.abs(user_sent_emb[id] - user_intent_emb[id]) for id in range(np.size(user_sent_emb, 0))])

    def canberra(self, user_sent_emb, user_intent_emb):
        return sum(
            [np.abs(user_sent_emb[id] - user_intent_emb[id]) / (np.abs(user_sent_emb[id]) + np.abs(user_intent_emb[id]))
             for id in range(np.size(user_sent_emb, 0))])

    def bray_curtis(self, user_sent_emb, user_intent_emb):
        return sum([np.abs(user_sent_emb[id] - user_intent_emb[id]) for id in range(np.size(user_sent_emb, 0))]) / sum(
            [np.abs(user_sent_emb[id] + user_intent_emb[id]) for id in range(np.size(user_sent_emb, 0))])

    def metric(self, user_sent_emb, user_intent_emb):
        return 0

    def t_sne(self, user_sent_emb, user_intent_emb_array):
        score_intent_emb = []
        sum_gauss_emb_array = 0
        for user_intent_emb in user_intent_emb_array:
            gauss = self.gauss(user_sent_emb, user_intent_emb)
            score_intent_emb.append(gauss)
            sum_gauss_emb_array += gauss

        print([score / sum_gauss_emb_array for score in score_intent_emb])
        return max([score / sum_gauss_emb_array for score in score_intent_emb])

    def kl_divergence(self, user_sent_emb, user_intent_emb):
        return sum(
            user_sent_emb[i] * np.log(user_sent_emb[i] / user_intent_emb[i]) for i in range(np.size(user_sent_emb, 0)))

    def kl_information(self, user_sent_emb, user_intent_emb):
        return 1 - self.kl_divergence(user_sent_emb, user_intent_emb)
