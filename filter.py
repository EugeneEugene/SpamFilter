from itertools import islice
from corpus import Corpus
import re, os
from trainingcorpus import TrainingCorpus

__author__ = 'eygene'


class MyFilter:
    def __init__(self):
        self.dic_of_spam = {}
        self.dic_of_ham = {}
        self.sorted_dic = {}
        self.dic_of_all = {}
        self.black_list = []
        self.white_list = []
        self.dic_of_probability = {}
        self.spam_counter = 0
        self.ham_counter = 0
        self.TrainingCorpus = ""

    def tokenization(self, body):
        list_of_tokens = []
        body = body.lower()
        pattern = r"""[a-z$'\-''0-9]+"""
        compiledre = re.compile(pattern)
        body_without_comments = re.sub("(<!--.*?-->)", "", body)
        tokens = compiledre.findall(body_without_comments)
        for element in tokens:
            if not element.isdigit():
                if element not in list_of_tokens:
                    if not element.isdigit() and len(element) >= 3:  # room for improvments
                        list_of_tokens.append(element)
        return list_of_tokens

    def get_email_adress(self, body):
        pars_for_adress = re.findall(r"From:+\s.+", body)
        get_str_with_adress = ''.join(pars_for_adress)
        address = re.findall(r"\w+@\w+.\w+", get_str_with_adress)
        return address

    def get_ham_dic(self):
        for filename, body in self.TrainingCorpus.hams():
            self.ham_counter += 2
            self.white_list.append(self.get_email_adress(body))
            body = self.tokenization(body)
            for element in body:
                if element not in self.dic_of_ham.keys():
                    self.dic_of_ham[element] = 2
                else:
                    self.dic_of_ham[element] += 2
                if element not in self.dic_of_all.keys():
                    self.dic_of_all[element] = 2
                else:
                    self.dic_of_all[element] += 2

    def get_spam_dic(self):
        for filename, body in self.TrainingCorpus.spams():
            self.spam_counter += 1
            self.black_list.append(self.get_email_adress(body))
            body = self.tokenization(body)
            for element in body:
                if element not in self.dic_of_spam.keys():
                    self.dic_of_spam[element] = 1
                else:
                    self.dic_of_spam[element] += 1
                if element not in self.dic_of_all.keys():
                    self.dic_of_all[element] = 1
                else:
                    self.dic_of_all[element] += 1

    def get_threshold(self):
        arr_to_del = {}
        for element in self.dic_of_all.keys():
            if self.dic_of_all[element] < 5:
                arr_to_del[element] = self.dic_of_all[element]
        for element in arr_to_del.keys():
            del self.dic_of_all[element]

    def grahams_technique(self, word):
        if word in self.dic_of_all.keys():
            if word not in self.dic_of_spam.keys():
                return 0.0100
            if word not in self.dic_of_ham.keys():
                return 0.9900
            else:
                word_in_spam = self.dic_of_spam[word]
                word_in_ham = self.dic_of_ham[word]
                return (word_in_spam / self.spam_counter) / (
                    (word_in_spam / self.spam_counter) + (word_in_ham / self.ham_counter))
        else:
            return 0.4

    def robinsons_technique(self, word):
        if word in self.dic_of_all:
            n = self.dic_of_all[word]
        else:
            n = 0
        x = 0.4
        s = 1
        return (s * x + n * self.grahams_technique(word)) / (s + n)

    def get_interestingness_in_mail(self, body):
        i = 0
        body = self.tokenization(body)
        self.dic_of_probability = {}
        dic_of_interestingness = {}
        for token in body:
            self.dic_of_probability[token] = self.grahams_technique(token)
        for element in self.dic_of_probability.keys():
            dic_of_interestingness[element] = abs(0.5 - self.dic_of_probability[element])
        list_of_interestingness = sorted(dic_of_interestingness, key=dic_of_interestingness.get, reverse=True)
        self.sorted_dic = {}
        for element in list_of_interestingness:
            i += 1
            self.sorted_dic[element] = dic_of_interestingness[element]
            if i == 15:
                break

    def bayesian_combination(self, body):
        product = 1
        inverse_product = 1
        self.get_interestingness_in_mail(body)
        for element in self.sorted_dic.keys():
            product *= self.dic_of_probability[element]
            inverse_product *= 1 - self.dic_of_probability[element]
        self.sorted_dic = {}
        return product / (product + inverse_product)

    def train(self, train_corpus_dir):
        self.pretratin()
        self.TrainingCorpus = TrainingCorpus(train_corpus_dir)
        self.get_ham_dic()
        self.get_spam_dic()
        self.get_threshold()

    def pretratin(self):
        self.TrainingCorpus = TrainingCorpus("/Users/eygene/Desktop/spam-data-12-s75-h25/3")
        self.get_spam_dic()
        self.TrainingCorpus = TrainingCorpus("/Users/eygene/Desktop/spam-data-12-s75-h25/4")
        self.get_ham_dic()
        self.get_tokens()

    def test(self, test_corpus_dir):
        test_corpus = Corpus(test_corpus_dir)
        with open(os.path.join(test_corpus_dir, '!prediction.txt'), 'w+') as a_file:
            for filename, body in test_corpus.emails():
                if self.bayesian_combination(body) > 0.9 or self.get_email_adress(body) in self.black_list:
                    decision = "SPAM"

                else:
                    if self.get_email_adress(body) in self.white_list:
                        decision = "OK"
                    else:
                        decision = "OK"
                a_file.write(filename + " " + decision + '\n')

    def get_tokens(self):
        with open(os.path.join("/Users/eygene/Desktop/spam-data-12-s75-h25/1", '!tokens.txt'), 'w+') as a_file:
            for element in a:
                if element in self.dic_of_ham:
                    ham = self.dic_of_ham[element]
                else:
                    next(self.dic_of_ham)
                if element in self.dic_of_spam:
                    spam = self.dic_of_spam[element]
                else:
                    next(self.dic_of_spam)
                a_file.write(element + " " + str(ham) + " " + str(spam) + '\n')
