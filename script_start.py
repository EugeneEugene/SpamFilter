__author__ = 'eygene'
from filter import MyFilter
from quality import compute_quality_for_corpus
import time , os
from corpus import Corpus

def set_truth(path):
    f = open(os.path.join(path, "!truth.txt"), 'wt')
    a = Corpus('/Users/eygene/Desktop/spam-data-12-s75-h25/3')
    for name, body in a.emails():
        f.write(name + ' ' + 'SPAM' + '\n')

def set_truth2(path):
    f = open(os.path.join(path, "!truth.txt"), 'wt')
    a = Corpus('/Users/eygene/Desktop/spam-data-12-s75-h25/4')
    for name, body in a.emails():
        f.write(name + ' ' + 'OK' + '\n')

def get_error(path):
    a_dic = {}
    b_dic = {}
    with open(os.path.join(path, "!truth.txt")) as truth:
        for a_line in truth:
            a_list = a_line.strip().split()
            a_dic[a_list[0]] = a_list[1]
    with open(os.path.join(path, "!prediction.txt")) as pred:
        for b_line in pred:
            b_list = b_line.strip().split()
            b_dic[b_list[0]] = b_list[1]



if __name__ == '__main__':
    train_corpus = '/Users/eygene/Desktop/spam-data-12-s75-h25/1'
    test_corpus = '/Users/eygene/Desktop/spam-data-12-s75-h25/2'

    filter = MyFilter()
    filter.train(train_corpus)
    filter.test(test_corpus)


    print('1>2: ' ,compute_quality_for_corpus(test_corpus))
    filter = MyFilter()
    filter.train(test_corpus)
    filter.test(train_corpus)
    print('2->1: ' ,compute_quality_for_corpus(train_corpus))
    filter = MyFilter()
    filter.train(test_corpus)
    filter.test(test_corpus)
    print('2->2: ', compute_quality_for_corpus(test_corpus))
    get_error(test_corpus)
    filter = MyFilter()
    filter.train(train_corpus)
    filter.test(train_corpus)
    print('1->1: ' ,compute_quality_for_corpus(train_corpus))


   # print("time: ",time.clock() - start)
   # filter = MyFilter()
   # filter.train('/Users/eygene/Desktop/spam-data-12-s75-h25/2')
   # filter.test('/Users/eygene/Desktop/spam-data-12-s75-h25/1')
   # print('2->1: ',compute_quality_for_corpus("/Users/eygene/Desktop/spam-data-12-s75-h25/1/"))