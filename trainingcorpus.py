__author__ = 'eygene'
import utils, os, random, corpus


class TrainingCorpus(corpus.Corpus):
    def __init__(self, path_to_train):
        self.path_to_train = path_to_train
        self.path_to_truth = os.path.join(path_to_train, '!truth.txt')
        self.truth_dic = utils.read_classification_from_file(self.path_to_truth)

    def get_class(self, path):
        if '!' not in path:
            if self.is_ham(path):
                return 'OK'
            if self.is_spam(path):
                return 'SPAM'

    def is_ham(self, path):
        if self.truth_dic[path] == 'OK':
            return True
        else:
            return False

    def is_spam(self, path):
        if self.truth_dic[path] == 'SPAM':
            return True
        else:
            return False

    def spams(self):
        for file_names in os.listdir(self.path_to_train):
            if self.get_class(file_names) == 'SPAM':
                with open(os.path.join(self.path_to_train, file_names),  encoding="ISO-8859-1") as a_file:
                    body = a_file.read()
                    yield (file_names, body)

    def hams(self):
        for file_names in os.listdir(self.path_to_train):
            if self.get_class(file_names) == 'OK':
                with open(os.path.join(self.path_to_train, file_names),  encoding="ISO-8859-1") as a_file:
                    body = a_file.read()
                    yield (file_names, body)

    def pre_spams(self):
        for file_names in os.listdir("/Users/eygene/Desktop/spam-data-12-s75-h25/3"):
            with open(os.path.join("/Users/eygene/Desktop/spam-data-12-s75-h25/3", file_names),
                      encoding="ISO-8859-1") as a_file:
                body = a_file.read()
                yield (file_names, body)
