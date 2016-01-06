__author__ = 'eygene'
import re
from collections import Counter
def math(ts,ti, sh, ih):
         p = (sh / ts) / ((sh / ts) + (ih / ti))
         print(p)
         return (1*0.5 + (ts + ti)*p)/ (1+ts+ti)
if __name__=="__main__":
        pattern = r"""[a-z$'\-''0-9]+"""
        compiledre = re.compile(pattern)
        tokens = compiledre.findall("pr-er9-...fdfsf")
        print(tokens)