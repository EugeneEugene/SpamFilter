__author__ = 'eygene'
import os, quality, corpus


class BaseFilter:

    def delete_prediction(self):
        os.remove(os.path.join(self.path_to_corpus, "!prediction"))

    def train(self, path_to_corpus):
        pass

    def test(self, path_to_corpus):
        f = open(os.path.join(path_to_corpus, "!prediction.txt"), 'wt')
        for f_name, f_body in corpus.Corpus(path_to_corpus).emails():
            f.write(f_name + ' ' + 'OK' + '\n')


    def quality_s(self):
        return quality.compute_quality_for_corpus(self.path_to_corpus)
