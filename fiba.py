# -*- coding: utf-8 -*-
# author: zhihuaye@gmail.com

from pyquery import PyQuery as pq
import sys
import requests
from io import open

eabaurl="http://www.fiba.basketball/asiacup/2017/eaba/0606/China-Korea#tab=play_by_play"
eabahtml='./eaba.html'
boxurl='http://www.fiba.basketball/asiacup/2017/eaba/0606/China-Korea#tab=boxscore'
#TODO: need to parse boxurl to get realurl
realboxurl='http://www.fiba.basketball/en/Module/79afbb16-7c16-4786-87e9-480773a6746c/b1324899-5530-4e2e-90fd-b48bdfbdf8dd'
boxhtml='./box.html'

'''
rsp = requests.get(realboxurl)
with open(boxhtml, 'w+', encoding='utf-8') as f:
    f.write(rsp.text)
'''
with open(boxhtml, 'r') as f:
    html = f.read()
target = pq(html)
scores = list()

def getallinone():

    positions = [pos.text() for pos in target('tr td.pos').items() if pos.text()!='#']
    names = [name.text() for name in target('tr td.name a.player-profile-link').items() if name.text()!='Players']
    print(positions)
    print(names)

getallinone()
exit(-1)
'''
rsp = requests.get(eabaurl)
with open(eabahtml, 'w+', encoding='utf-8') as f:
    f.write(rsp.text)
'''


#use stored version
with open(eabahtml, 'r') as f:
    html = f.read()

target = pq(html)

infos = list()
for section in target('li.action-item').items():
    athlete = section('span.athlete-name').text()
    action = section('span.action-description').text()
    period = section('span.period').text()
    time = section('span.time').text()
    if athlete:
        one = (athlete, action, period, time)
        infos.append(one)

with open('./eaba.info','w+') as f:
    for info in infos:
        athlete, action, period, time = info
        f.write('{},{},{},{}\n'.format(athlete, action, period,time))