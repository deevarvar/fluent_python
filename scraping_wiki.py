# -*- coding=utf-8 -*-
# author: zhihuaye@gmail.com

"""
use pyquery instead of bs4 to scrape first table in
https://en.wikipedia.org/wiki/Comparison_of_text_editors


"""

from pyquery import PyQuery as pq
import sys
import requests
#import csv , csv unicoding is not supported well...as
import unicodecsv as csv


PY3k = sys.version_info >= (3,)
WIKIPAGEURL="https://en.wikipedia.org/wiki/Comparison_of_text_editors"
WIKIPAGE='./wiki.html'
CSV='./1sttable.csv'
tablepattern=".wikitable"


def gettable():
    try:
        rsp = requests.get(WIKIPAGEURL)
        if PY3k:
            with open(WIKIPAGE, 'w+', encoding='utf-8') as f:
                f.write(rsp.text)
                return rsp.text
        else:
            with open(WIKIPAGE, 'w+') as f:
                pagehtml = rsp.text.encode('utf-8')
                f.write(pagehtml)
                return pagehtml
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        sys.exit(-1)
    except requests.exceptions.ConnectionError as errc:
        print("Connection Error:", errc)
        sys.exit(-1)
    except requests.exceptions.Timeout as errt:
        print("TimeOut:", errt)
        sys.exit(-1)
    except requests.exceptions.RequestException as errr:
        print("RequestExeptions:", errr)
        sys.exit(-1)
    except:
        etype = sys.exc_info()[0]
        estr = sys.exc_info()[1]
        print("Exceptions: {} {}".format(etype, estr))
        sys.exit(-1)

def writecsv(htmlstr):
    #unicodecsv expect a bytestream
    with open(CSV, 'wb') as cf:
        writer = csv.writer(cf, encoding='utf-8')
        #pq filename seems no encoding options, do not use pq filename
        page = pq(htmlstr)
        #get first table
        table = page(tablepattern).eq(0)
        for tr in table('tr').items():
            #print(''.join('_' for i in range(30)))
            #each tr will have th or td
            onerow = []
            for telement in tr('th, td').items():
                onerow.append(telement.text())
            writer.writerow(onerow)

if  __name__ == '__main__':
    html = gettable()
    writecsv(html)