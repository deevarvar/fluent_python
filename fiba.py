# -*- coding: utf-8 -*-
# author: zhihuaye@gmail.com

from pyquery import PyQuery as pq
import sys
import requests
from io import open
from operator import itemgetter
import os
import argparse


qualifierurl="http://www.fiba.basketball/basketballworldcup/2019/asian-qualifiers/fullschedule"
FIBAURL="http://www.fiba.basketball"
DATADIR='./data'
qhtml=os.path.join(DATADIR, 'qualifier.html')

TEAMSELECTORS = ["positions", "names", "min", "pts", "field-goals", "field-goals-2p", "field-goals-3p", "free-throw",
            "reb-offence", "reb-defence", "reb-total", "personal-fouls", "turnovers",
            "assists", "steals", "block-shots", "plus-minus", "efficiency"]

eabaurl="http://www.fiba.basketball/asiacup/2017/eaba/0606/China-Korea#tab=play_by_play"
eabahtml='./eaba.html'
boxurl='http://www.fiba.basketball/asiacup/2017/eaba/0606/China-Korea#tab=boxscore'
#TODO: need to parse boxurl to get realurl
realboxurl='http://www.fiba.basketball/en/Module/79afbb16-7c16-4786-87e9-480773a6746c/b1324899-5530-4e2e-90fd-b48bdfbdf8dd'
boxhtml='./box.html'
#SPECIAL CASE:
#http://www.fiba.basketball//en/Module/943235cf-8d74-4311-8e8d-90c6b336a861/0b39b80b-f2e3-448a-9c1d-019e14d3d68b
# 12 player, one line is not good
newboxhtml=os.path.join(DATADIR, 'China-Lebanon_box.html')



'''
rsp = requests.get(qualifierurl)
with open(qhtml, 'w+', encoding='utf-8') as f:
    f.write(rsp.text)

'''
from time import strftime, strptime


def getbox(html=None):
    # entry is html
    if html:
        Aplayerbox, Ateambox, Aplayerinfo = getteaminfo(html('section.box-score_team-A'))
        Bplayerbox, Bteambox, Bplayerinfo = getteaminfo(html('section.box-score_team-B'))
        '''
        print(Aplayerbox)
        print(Bplayerbox)
        print(Ateambox)
        print(Bteambox)
        print(Aplayerinfo)
        print(Bplayerinfo)
        '''
        print('TeamA')
        sortplayer(Aplayerbox,kw='pts', num=args.num)
        print('TeamB')
        sortplayer(Bplayerbox, kw='pts', num=args.num)
        #sortplayer(Aplayerbox,kw="field-goals-3p")

def sortfunc(elem, kw):
    if kw in ["field-goals", "field-goals-2p", "field-goals-3p", "free-throw"]:
        #'1/2 50%'
        return elem.split(' ')[1]
    elif kw == 'min':
        return elem
    else:
        return int(elem)

def sortplayer(playerbox, kw='pts', num=None):
    # reformat the playerbox
    playerlist = []
    for index in range(len(playerbox["pos"])):
        oneplayer = dict()
        for field,value in playerbox.items():
            oneplayer[field] = value[index]
        playerlist.append(oneplayer)
    sortedlist = sorted(playerlist, key=lambda elem: sortfunc(elem[kw], kw), reverse=True)
    #print(sortedlist[:num])
    maxnamelen = 0
    for leader in sortedlist[:num]:
        if len(leader['name']) > maxnamelen:
            maxnamelen = len(leader['name'])

    for leader in sortedlist[:num]:
        #format string is like {name:{fill}{align}{width}}
        print("{name:{fill}{align}{namewidth}}, {pts:{fill}{align}3}, {plusminus:{fill}{align}3},{efficiency:{fill}{align}2}".format(name=leader['name'], pts=leader['pts'] ,
                                                               plusminus=leader['plus-minus'], efficiency=leader['efficiency'], namewidth=maxnamelen, fill=' ', align="<"))


def cleandata(playerbox):
    #in some special case, playerbox element length is not equal...
    if len(playerbox["min"]) == len(playerbox["pts"]):
        return playerbox
    else:
        # iterate to clean data
        # Logic may not be complete
        badindexes = []
        for index, min in enumerate(playerbox['min']):
            #length should be 12:24
            if len(min) != 5:
                print('badindex {}'.format(index))
                badindexes.append(index)
        if len(badindexes) > 0:
            print(playerbox['name'])
        '''
        bad way, playerbox is changing!!!
        for _ in badindexes:
            del playerbox['name'][_]
            del playerbox['pos'][_]
            del playerbox['min'][_]
        '''
        #use listcomp
        playerbox['name'] = [element for i, element in enumerate(playerbox['name']) if i not in badindexes]
        playerbox['pos'] = [element for i, element in enumerate(playerbox['pos']) if i not in badindexes]
        playerbox['min'] = [element for i, element in enumerate(playerbox['min']) if i not in badindexes]
        return playerbox


def getteaminfo(html=None):
    playerbox = {}
    teambox ={}
    playerinfo = {}
    # structure is similar:
    # pos, name seems not that easy to summarize
    playerbox['pos'] = [pos.text() for pos in html('tr td.pos').items()]
    playerbox['name'] = [name.text() for name in html('tr td.name a.player-profile-link').items()]

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

    #add logic to clean
    playerbox = cleandata(playerbox)
    #for key,value in playerbox.items():
     #   print('playerbox {} length is {} , detail is {}'.format(key, len(value),value))

    # add logic to get team total
    for tdselector in TEAMSELECTORS:
        #only one element
        teambox[tdselector] = html('tr.team-totals').find('td.'+tdselector).text()
    #print(teambox)
    # get coach, assistant, starter
    playerinfo["coaches"] = html('div.coaches-list span.value').text()
    playerinfo["assistants"] = [assistant.text() for assistant in html('div.assistants-list span.value').items()]
    playerinfo["starters"] = [start.text() for start in html('tr.x--player-is-starter td.name').items()]
    return playerbox, teambox, playerinfo

# date , match url
def getmatches():
    matchinfoes = list()
    for daydiv in target('li#Past div.day_content').items():
        matchday = daydiv('.section_header h4').text()
        #get day of week

        dow = strftime('%A', strptime(matchday, '%d %B %Y'))
        #print("{} {}".format(dow, matchday))
        from collections import namedtuple
        #use namedtuple to record
        Matchtuple = namedtuple('Matchtuple', ["date",'matchurl','group', 'venue'])
        matchinfoes = matchinfoes + [Matchtuple(matchday, a.attr('href'), a.attr('data-group'), a.attr('data-venues'))for a in daydiv('a.score_cell').items()]
        #print("len is {}, {}".format(len(matchinfos),matchinfos))
    return matchinfoes


def getupcomingmatch():
    pass


def getmatchbydate(matchinfoes=None, date='1/1/2018'):
    for matchinfo in matchinfoes:
        day, matchurl, group, venue = matchinfo
        if strptime(day, "%d %B %Y") > strptime(date, '%d/%m/%Y'):
            print('{}, {}'.format(day, matchurl))
            urlprefix = matchurl.split('/')[-1]
            htmlfile = os.path.join(DATADIR,urlprefix+'.html')
            if os.path.isfile(htmlfile) is False:
                rsp = requests.get(FIBAURL + matchurl)
                with open(htmlfile, 'w+', encoding='utf-8') as f:
                    f.write(rsp.text)

            with open(htmlfile, 'r', encoding='utf-8') as f:
                html = f.read()
            target = pq(html)
            #get the box page
            ajaxurl = target('div#gamepage_tabs li[data-tab-content=boxscore]').attr('data-ajax-url')
            if ajaxurl:
                print(ajaxurl)
                boxfile = os.path.join(DATADIR,urlprefix+'_box.html')
                if os.path.isfile(boxfile) is False:
                    rsp = requests.get(FIBAURL + ajaxurl)
                    with open(boxfile, 'w+', encoding='utf-8') as f:
                        f.write(rsp.text)
                with open(boxfile, 'r', encoding='utf-8') as f:
                    html = f.read()
                target = pq(html)
                getbox(html=target)
            else:
                print("no match details for {}".format(matchurl.split('.')[0]))


parser = argparse.ArgumentParser(prog='asia_qualifier')
parser.add_argument('--date',help="the start of date game will crawl, format is day/month/year, 1/12/2018",default="1/12/2018")
parser.add_argument('--num', type=int,help="top N player, default is 3", default=3)
args = parser.parse_args()



with open(qhtml, 'r',encoding='utf-8') as f:
    html = f.read()
target = pq(html)

matchinfoes = getmatches()
getmatchbydate(matchinfoes, date=args.date)

exit(-1)


'''
rsp = requests.get(realboxurl)
with open(boxhtml, 'w+', encoding='utf-8') as f:
    f.write(rsp.text)
'''
with open(newboxhtml, 'r', encoding='utf-8') as f:
    html = f.read()
target = pq(html)
getbox(html=target)


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