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
import errno
from timeit import default_timer as timer
import shutil
from concurrent import futures

FLAG_BASEURL='https://www.countries-ofthe-world.com/'
INDEX_URI='flags-of-asia.html'
FLAGPAGE='./flags.html'
FLAGDIR='./flags'
Headers = {
    'user-agent': "Mozilla"
}

def benchmark(func):
    """
    decorator to print the time a function executes.
    :param func: 
    :return: 
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = timer()
        res = func(*args, **kwargs)
        print("{0} takes {1:.7f} seconds".format(func.__name__, timer() - start))
        return res
    return wrapper

@benchmark
def hello():
    print("start to run")


@benchmark
def mkdirp(dirname):
    try:
        os.makedirs(dirname)
    except OSError as error:
        if error.errno == errno.EEXIST and os.path.isdir(dirname):
            pass
        else:
            raise

@benchmark
def getflagpage():
    rsp = requests.get(FLAG_BASEURL + INDEX_URI, headers=Headers)
    rsp.raise_for_status()

    with open(FLAGPAGE,'w+') as handle:
        handle.write(rsp.text)

@benchmark
def getoneflag(imgelement):
    imgurl = FLAG_BASEURL + imgelement.get('src')
    #flags-normal/flag-of-Afghanistan.png
    imgname = FLAGDIR + '/' + imgelement.get('src').split('/')[1]
    rsp = requests.get(imgurl, headers=Headers)
    rsp.raise_for_status()
    # open as binary and get content
    with open(imgname, 'wb') as handle:
        handle.write(rsp.content)

@benchmark
def getcountryflags():
    page = pq(filename=FLAGPAGE)
    #listcomp, lxml element
    #imglist = [ i.get('src') for i in page('table').find('img')]
    #print(imglist)
    for imgelement in page('table').find('img'):
        getoneflag(imgelement)

@benchmark
def futuresgetflags():
    page = pq(filename=FLAGPAGE)
    workers = 20
    imgelementlist = [element for element in page('table').find('img')]
    with futures.ThreadPoolExecutor(workers) as executor:
        executor.map(getoneflag, imgelementlist)


if __name__ == '__main__':
    shutil.rmtree(FLAGDIR)
    mkdirp(FLAGDIR)
    getflagpage()
    getcountryflags()
    #futuresgetflags()
