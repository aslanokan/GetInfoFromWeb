# -*- coding: utf-8 -*-

from lxml import html
import requests

artists = {}
songs = {}

def getSongs(link):
    try:
        page = requests.get(link)
    except requests.exceptions.ConnectionError, e:
        print e

    tree = html.fromstring(page.content)

    artistName = tree.xpath("//td[@class = 'chartlist-name']/span/span/a/text()")
    songName = tree.xpath("//td[@class = 'chartlist-name']/span/a/text()")
    for i in range(len(artistName)):
        artist = artistName[i]
        song = songName[i]
        if artist not in artists:
            artists[artist] = {"Total": 1}
            artists[artist][song] = 1
        else:
            if song not in artists[artist]:
                artists[artist][song] = 1
            else:
                artists[artist][song] += 1
            artists[artist]["Total"] += 1

getSongs("https://www.last.fm/user/Filojiston/library")
for i in range(2, 10):
    getSongs("https://www.last.fm/user/Filojiston/library" + "?page=" + str(i))

print "\n\n\n"
for i in artists:
    print i, "(Total:", artists[i]["Total"], ")", ":"
    for q in artists[i]:
        if q != "Total":
            print "\t", artists[i][q], "=>", q
