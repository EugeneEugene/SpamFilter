__author__ = 'eygene'


class BinaryConfusionMatrix:
    def __init__(self, pos_tag, neg_tag):
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0
        self.pos_tag = pos_tag
        self.neg_tag = neg_tag

    def as_dict(self):
        return {'tp': self.TP, 'tn': self.TN, 'fp': self.FP, 'fn': self.FN}

    def update(self, truth, prediction):
        if (prediction != self.pos_tag and prediction != self.neg_tag) or \
                (truth != self.pos_tag and truth != self.neg_tag):
            raise ValueError

        if prediction == self.pos_tag:
            if truth == prediction:
                self.TP += 1
            else:
                self.FP += 1
        if prediction == self.neg_tag:
            if truth == prediction:
                self.TN += 1
            else:
                self.FN += 1

    def compute_from_dicts(self, truth_dict, pred_dict):
        for keys in truth_dict.keys():
            self.update(truth_dict[keys], pred_dict[keys])
        print("FP: ", self.FP, "FN: ", self.FN)