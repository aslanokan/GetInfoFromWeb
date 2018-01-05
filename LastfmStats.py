# -*- coding: utf-8 -*-

from lxml import html
import requests

def getInfo(link):
    try:
        page = requests.get(link)
    except requests.exceptions.ConnectionError, e:
        print e

    tree = html.fromstring(page.content)

    artistNames = tree.xpath("//td[@class = 'chartlist-name']/span/span/a/text()")
    songNames = tree.xpath("//td[@class = 'chartlist-name']/span/a/text()")
    dates = tree.xpath("//td[@class = 'chartlist-timestamp']/span/@title")

    lis = []
    for i in range(len(artistNames)):
        lis.append([artistNames[i], songNames[i], dates[i]])

    return lis

def songInfo(info):
    songs = {}
    for i in info:
        artist = i[0]
        song = i[1]
        date = i[2]
        if song not in songs:
            songs[song] = [artist, [date]]
        else:
            songs[song][1].append(date)
    return songs

def artistInfo(info):
    artists = {}
    for i in info:
        artist = i[0]
        song = i[1]
        date = i[2]
        if artist not in artists:
            artists[artist] = {song: [date]}
        else:
            if song not in artists[artist]:
                artists[artist][song] = [date]
            else:
                artists[artist][song].append(date)

    return artists

def getLink(userName, pageNumber=1):
    link ="https://www.last.fm/user/" + userName + "/library"
    if pageNumber > 1:
        link += "?page=" + str(pageNumber)
    return link

user = "SilencedFear"

info = []
for i in range(1, 2):
    info += getInfo(getLink(user, i))

songs = songInfo(info) #dictionary
artists = artistInfo(info) #dictionary

def printAllInfo():
    for i in artists:
        print i
        for q in artists[i]:
            print "  ", q
            for k in artists[i][q]:
                print "     ", k
        print

def searchForArtist(x):
    if x in artists:
        songsOfX = artists[x]
        return songsOfX

def searchForSong(x):
    if x in songs:
        song = songs[x]
        bandName = song[0]
        dates = song[1]
        return bandName, dates

printAllInfo()

while(True):
    print searchForSong(raw_input(": "))
