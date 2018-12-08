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

def getboxdemo():

    #pos, name seems not that easy to summarize
    positions = [pos.text() for pos in target('tr td.pos').items()]
    names = [name.text() for name in target('tr td.name a.player-profile-link').items()]

    #skin total min, normal min is 23:05
    mins = [min.text() for min in target('tr').not_('.team-totals').find('td.min').items() if min.text()]
    pts = [pt.text() for pt in target('tr').not_('.team-totals').find('td.pts').items() if pt.text()]
    # format: 12/24 50%
    fieldgoals = [fg.text() for fg in target('tr').not_('.team-totals').find('td.field-goals').items() if fg.text()]
    twopointfgs = [twofg.text() for twofg in target('tr').not_('.team-totals').find('td.field-goals-2p').items() if twofg.text()]
    threepointfgs = [threefg.text() for threefg in target('tr').not_('.team-totals').find('td.field-goals-3p').items() if
                     threefg.text()]
    freethrows = [freethrow.text() for freethrow in target('tr').not_('.team-totals').find('td.free-throw').items() if
                  freethrow.text()]
    print(positions)
    print(names)
    print(mins)
    print(pts)
    print(fieldgoals)
    print(twopointfgs)
    print(threepointfgs)
    print(freethrows)

def getbox(html=None):
    # entry is html
    if html:
        Aplayerbox, Ateambox, Aplayerinfo = getteaminfo(html('section.box-score_team-A'))
        Bplayerbox, Bteambox, Bplayerinfo = getteaminfo(html('section.box-score_team-B'))
        print(Aplayerbox)
        print(Bplayerbox)
        print(Ateambox)
        print(Bteambox)
        print(Aplayerinfo)
        print(Bplayerinfo)


def sortinfo(kw='pts'):
    pass


def getteaminfo(html=None):
    playerbox = {}
    teambox ={}
    playerinfo = {}
    # structure is similar:
    # pos, name seems not that easy to summarize
    playerbox['positions'] = [pos.text() for pos in html('tr td.pos').items()]
    playerbox['names'] = [name.text() for name in html('tr td.name a.player-profile-link').items()]

    # exclude team rebounds etc..
    onetdsels = ["reb-offence", "reb-defence", "reb-total", "personal-fouls", "turnovers"]

    for tdsel in onetdsels:
        trs = html('tr').not_('.team-totals, .coaches')
        playerbox[tdsel] = [data.text() for data in trs.find('td.'+tdsel).items() if data.text()]

    # the other field  can be summarized by
    # non tr class team-totals , td class
    tdsels = ["min", "pts", "field-goals", "field-goals-2p", "field-goals-3p", "free-throw",
              "assists", "steals", "block-shots", "plus-minus", "efficiency"]
    for tdselector in tdsels:
        trs = html('tr').not_('.team-totals')
        playerbox[tdselector] = [data.text() for data in trs.find('td.'+tdselector).items() if data.text()]

    #for key,value in playerbox.items():
     #   print('playerbox {} length is {} , detail is {}'.format(key, len(value),value))

    # add logic to get team total
    teamsels = ["min", "pts", "field-goals", "field-goals-2p", "field-goals-3p", "free-throw",
              "reb-offence", "reb-defence", "reb-total", "personal-fouls", "turnovers",
                "assists", "steals", "block-shots", "plus-minus", "efficiency"]
    for tdselector in teamsels:
        #only one element
        teambox[tdselector] = html('tr.team-totals').find('td.'+tdselector).text()
    #print(teambox)
    # get coach, assistant, starter
    playerinfo["coaches"] = html('div.coaches-list span.value').text()
    playerinfo["assistants"] = [assistant.text() for assistant in html('div.assistants-list span.value').items()]
    playerinfo["starters"] = [start.text() for start in html('tr.x--player-is-starter td.name').items()]
    return playerbox, teambox, playerinfo

getbox(html=target)

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