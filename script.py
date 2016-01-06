__author__ = 'eygene'
import simplefilters
if __name__ == "__main__": 
    n_f = simplefilters.NaiveFilter()
    n_f.test()
    print(n_f.quality_s())

