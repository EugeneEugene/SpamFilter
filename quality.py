__author__ = 'eygene'
import utils, os, confmat


def quality_score(tp, tn, fp, fn):
    return (tp + tn) / (tp + tn + 10 * fp + fn)


def compute_quality_for_corpus(corpus_dir):
    truth = utils.read_classification_from_file(os.path.join(corpus_dir, '!truth.txt'))
    prediction = utils.read_classification_from_file(os.path.join(corpus_dir, '!prediction.txt'))
    mat = confmat.BinaryConfusionMatrix('SPAM', 'OK')
    mat.compute_from_dicts(truth, prediction)
    p = mat.as_dict()
    return quality_score(p['tp'], p['tn'], p['fp'], p['fn'])
