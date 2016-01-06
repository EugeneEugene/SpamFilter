__author__ = 'eygene'
line_number = 0


def read_classification_from_file(FILENAME):
    a_dic = {}
    with open(FILENAME, encoding = "ISO-8859-1") as a_file:
        for a_line in a_file:
            a_list = a_line.strip().split()
            a_dic[a_list[0]] = a_list[1]
    return a_dic
