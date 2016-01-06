import os

__author__ = 'eygene'


class Corpus:
    def __init__(self, path):
        self.path = path

    def emails(self):
        for filename in os.listdir(self.path):
            if '!' not in filename:
                # I run this code on OS X so I have to skip .Ds_Store file
                if '.DS_Store' not in filename:
                    if 'tokens.txt' not in filename:
                        with open(os.path.join(self.path, filename), encoding = "ISO-8859-1") as a_file:
                            body = a_file.read()
                            yield (filename, body)
