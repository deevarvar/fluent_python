# -*- coding=utf-8 -*-
# author: zhihuaye@gmail.com

"""
classic example to count word summary of file
1. generate a file with random words
2. count words
"""

import random
import string
import datetime
import re
import os
from collections import defaultdict

def randomstr(ulimit=5):
    """

    :param ulimit:
    :return:
    """
    if ulimit < 2:
        ulimit = 5
    strlen = random.randint(2, ulimit)
    #print("{0:2d}".format(ulimit))
    stringpool = string.ascii_letters + string.digits
    rstr = ''.join(random.choice(stringpool) for _ in range(strlen))
    return rstr


def wordsummary(file=__file__):
    words = defaultdict(list)
    if os.path.isfile(file):
        with open(file) as f:
            for lineno, line in enumerate(f, start=1):
                #print("lineno is {}, line is {}".format(lineno, line), end='')
                linewords = [oneword for oneword in line.split()]
                for lineword in linewords:
                    words[lineword].append(lineno)
    for key,value in words.items():
        print("word {}, num is {}".format(key,value))


def worddetails(file=""):
    words = defaultdict(list)
    if os.path.isfile(__file__):
        pattern = re.compile(r'\w+')
        with open(file) as f:
            for lineno, line in enumerate(f, start=1):
                for matchobj in re.finditer(pattern, line):
                    #manipulate matchobj
                    keyword = matchobj.group()
                    colnum = matchobj.start() + 1
                    words[keyword].append((lineno, colnum))

    for key, value in words.items():
          print("word {}, occurence is {}".format(key,value))

if __name__ == '__main__':
    print(randomstr(5))
    #wordsummary()
    worddetails(file='./test.txt')