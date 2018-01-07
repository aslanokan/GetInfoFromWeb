# -*- coding: utf-8 -*-

from lxml import html
import requests

class UserListerner():
    def __init__(self, userName):
        self.information = []
        self.songs = {}
        self.artists = {}
        self.userName = userName
        self.startPage = 1
        self.stopPage = 2


        for i in range(self.startPage, self.stopPage):
            self.getInformation(self.getLink(i))

        self.songInfo(self.information) #dictionary
        self.artistInfo(self.information) #dictionary


    def getLink(self, pageNumber=1):
        link ="https://www.last.fm/user/" + self.userName + "/library"
        if pageNumber > 1:
            link += "?page=" + str(pageNumber)
        return link

    def getInformation(self, link):
        try:
            page = requests.get(link)
        except requests.exceptions.ConnectionError, e:
            print e

        tree = html.fromstring(page.content)

        artistNames = tree.xpath("//td[@class = 'chartlist-name']/span/span/a/text()")
        songNames = tree.xpath("//td[@class = 'chartlist-name']/span/a/text()")
        dates = tree.xpath("//td[@class = 'chartlist-timestamp']/span/@title")

        for i in range(len(artistNames)):
            self.information.append([artistNames[i], songNames[i], dates[i]])

    def songInfo(self, info):
        for i in info:
            artist = i[0]
            song = i[1]
            date = i[2]
            if song not in self.songs:
                self.songs[song] = [artist, [date]]
            else:
                self.songs[song][1].append(date)

    def artistInfo(self, info):
        for i in info:
            artist = i[0]
            song = i[1]
            date = i[2]
            if artist not in self.artists:
                self.artists[artist] = {song: [date]}
            else:
                if song not in self.artists[artist]:
                    self.artists[artist][song] = [date]
                else:
                    self.artists[artist][song].append(date)

    def searchForArtist(x):
        if x in self.artists:
            songsOfX = self.artists[x]
            return songsOfX

    def searchForSong(x):
        if x in self.songs:
            song = self.songs[x]
            bandName = song[0]
            dates = song[1]
            return bandName, dates

Okan = UserListerner("Filojiston")
Lacin = UserListerner("LAcin98")

def listInfo(user):
    for i in user.artists:
        print i
        for q in user.artists[i]:
            print "\t", q
            for k in user.artists[i][q]:
                print "\t\t", k
        print

listInfo(Lacin)
