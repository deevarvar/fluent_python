# -*- coding=utf-8 -*-
# author: zhihuaye@gmail.com

"""
1. try to get flags
https://www.countries-ofthe-world.com/flags-of-the-world.html
2. find the sample url
https://www.countries-ofthe-world.com/flags-normal/flag-of-China.png
3. add UA to get file
"""

import sys
import os
from pyquery import PyQuery as pq
import requests
import time
import functools

FLAG_BASEURL='https://www.countries-ofthe-world.com/'
INDEX_URI='flags-of-asia.html'
FLAG_PREFIX='flags-normal/flag-of-'
FLAGFILE='./flags.html'


def benchmark(func):
    """
    decorator to print the time a function executes.
    :param func: 
    :return: 
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t = time.process_time()
        res = func(*args, **kwargs)
        print("{0} takes {1:.7f}".format(func.__name__, time.process_time() -t))
        return res
    return wrapper

@benchmark
def hello():
    print("start to run")

@benchmark
def getflagpage():
    headers = {
        'user-agent': "Mozilla"
    }
    rsp = requests.get(FLAG_BASEURL + INDEX_URI, headers=headers)
    rsp.raise_for_status()

    with open(FLAGFILE,'w+') as handle:
        handle.write(rsp.text)

@benchmark
def getcountry():
    d = pq(filename=FLAGFILE)
    #listcomp, lxml element
    imglist = [ i.get('src') for i in d('table').find('img')]
    print(imglist)

if __name__ == '__main__':
    hello()
    #getflagpage()
    getcountry()