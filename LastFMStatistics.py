# -*- coding: utf-8 -*-

from lxml import html
import requests

artists = {}

def getInfo(link):
    try:
        page = requests.get(link)
    except requests.exceptions.ConnectionError, e:
        print e

    tree = html.fromstring(page.content)

    artistNames = tree.xpath("//td[@class = 'chartlist-name']/span/span/a/text()")
    songNames = tree.xpath("//td[@class = 'chartlist-name']/span/a/text()")

    getAllSongs(artistNames, songNames)

def getLink(userName, pageNumber=1):
    link ="https://www.last.fm/user/" + userName + "/library"
    if pageNumber > 1:
        link += "?page=" + str(pageNumber)
    return link

def getAllSongs(artistNames, songNames):
    for i in range(len(artistNames)):
        artist = artistNames[i]
        song = songNames[i]
        if artist not in artists:
            artists[artist] = {song: 1}
        else:
            if song not in artists[artist]:
                artists[artist][song] = 1
            else:
                artists[artist][song] += 1

def listArtists(artists):
    for i in artists:
        print i

def listArtistsWithSongs(artists):
    for i in artists:
        print i, ":"
        songs = enumDictionary(artists[i])
        for q in range(len(songs)):
            print "  " + str(q+1) + "-> " + str(songs[q][0]) + "-" + songs[q][1]

def enumDictionary(dict):
    enumLis = []
    for i in dict:
        enumLis.append([dict[i], i])

    for i in range(len(enumLis)):
        for q in range(i):
            if enumLis[i-q][0] > enumLis[i-q-1][0]:
                temp = enumLis[i-q-1]
                enumLis[i-q-1] = enumLis[i-q]
                enumLis[i-q] = temp
    return enumLis

def getNumberOfSongs(artists):
    numOfSongs = 0
    numOfDiffSongs = 0
    for i in artists:
        for q in artists[i]:
            numOfSongs += artists[i][q]
            numOfDiffSongs += 1
    return (numOfSongs, numOfDiffSongs)

for i in range(1, 50):
    getInfo(getLink("Filojiston", i))

listArtistsWithSongs(artists)
print len(artists), "different artists"
print getNumberOfSongs(artists)[0], "songs"
print getNumberOfSongs(artists)[1], "different songs"
