__author__ = 'eygene'

import os, corpus, trainingcorpus, re, time, utils


class MyFilter:
    def __init__(self):
        self.time = time.time()
        self.bad_words = {}
        self.good_words = {}
        self.all_words = {}
        self.probability_dic = {}
        self.sh = 0
        self.ih = 0
        self.ts = 0
        self.ti = 0
        self.mail = ""
        self.white_list = []
        self.black_list = []
        self.mail = ""

    def tokenization(self, body):
        new = body.split('\n')
        for string in new:
            if string.startswith("From:"):
                split_string = string.split()
                for element in split_string:
                    if "@" in element:
                        element = element.replace("<", "")
                        element = element.replace(">", "")
                        element = element.replace('"', "")
                break
        self.mail = element
        tokens_done = []
        # remove all html comments
        pattern = r"""[a-z$/'0-9]+"""
        compiledre = re.compile(pattern)
        body_without_comments = re.sub("(<!--.*?-->)", "", body)
        tokens = compiledre.findall(body_without_comments)
        for element in tokens:
            if not element.isdigit():
                if element not in tokens_done:
                    tokens_done.append(element)
        return tokens_done

    def get_dic_of_spam_words(self):
        for filename, body in self.t_copus.spams():
            if self.mail not in self.black_list:
                self.black_list.append(self.mail)
            self.ts += 1
            a_body = self.tokenization(body)
            for element in a_body:
                if element in self.bad_words.keys():
                    self.bad_words[element] += 1
                else:
                    self.bad_words[element] = 1
        return self.bad_words

    def get_dic_of_ham_words(self):
        for filename, body in self.t_copus.hams():
            self.ti += 1
            a_body = self.tokenization(body)
            print("Filename: ",filename)
            p = re.findall(r"From:+\s.+", body)
            print("NASHEL: ", p)
            str = ''.join(p)
            lel = re.findall(r"\w+@\w+.\w+", str)
            print("ADRESS: ", lel)
            if self.mail not in self.white_list:
                self.white_list.append(self.mail)
            for element in a_body:
                if element in self.good_words.keys():
                    self.good_words[element] += 2
                else:
                    self.good_words[element] = 2
        return self.good_words

    def probability_of_spam(self, token):
        if token in self.good_words:
            self.ih = self.good_words[token]
        else:
            self.ih = 0
        if token in self.bad_words:
            self.sh = self.bad_words[token]
        else:
            self.sh = 0
        p = (self.sh / self.ts) / ((self.sh / self.ts) + (self.ih / self.ti))
        n = self.ih + self.sh
        return (1*0.4 + n * p)/(1 + n)
        #return p

    def get_prob_dic(self):
        for word in self.all_words.keys():
            self.probability_dic[word] = self.probability_of_spam(word)
        for element in self.probability_dic.keys():
            if self.probability_dic[element] == 0.0:
                self.probability_dic[element] = 0.0100
            if self.probability_dic[element] == 1.0:
                self.probability_dic[element] = 0.9900

    def get_all_words_in_emails(self):
        self.all_words = self.good_words.copy()
        self.all_words.update(self.bad_words)

    def mathematical_foundation(self, body):
        prob_dic_for_element = 0
        count = 0
        prob_dic_for_body = {}
        tokenization_body = self.tokenization(body)
        for element in tokenization_body:
            count += 1
            if element in self.probability_dic.keys():
                prob_dic_for_element += self.probability_dic[element]
            else:
                prob_dic_for_element += 0.4
        return prob_dic_for_element / count

    def pre_train_spam(self):
        for filename, body in self.t_copus.pre_spams():
            a_body = self.tokenization(body)
            for elements in a_body:
                if elements in self.bad_words.keys():
                    self.bad_words[elements] += 1
                else:
                    self.bad_words[elements] = 1

    def pre_train_ham(self):
        for filename, body in self.t_copus.pre_spams():
            a_body = self.tokenization(body)
            print("Filename: ",filename)
            p = re.findall(r"From:+\s+\w+@+\w+.+\w", "body")
            for elements in a_body:
                if elements in self.good_words.keys():
                    self.good_words[elements] += 1
                else:
                    self.good_words[elements] = 1


    def train(self, train_corpus_dir):
        self.t_copus = trainingcorpus.TrainingCorpus(train_corpus_dir)
        self.get_dic_of_ham_words()
        self.get_dic_of_spam_words()
        self.get_all_words_in_emails()
        self.get_prob_dic()

    def test(self, test_corpus_dir):
        a = corpus.Corpus(test_corpus_dir)
        with open(os.path.join(test_corpus_dir, '!prediction.txt'), 'w+') as a_file:
            for filename, body in a.emails():
                m_f = self.mathematical_foundation(body)

                if self.mathematical_foundation(body) > 0.4:
                    decision = "SPAM"
                else:
                    decision = "OK"
                a_file.write(filename + " " + decision + '\n')
