# -*- coding: utf-8 -*-

from lxml import html
import requests

class UserListerner():
    userNumber = 0

    def __init__(self, userName):
        UserListerner.userNumber += 1
        self.information = []
        self.songs = {}
        self.artists = {}
        self.userName = userName
        self.startPage = 1
        self.stopPage = 20

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

    def searchForArtist(self, x):
        if x in self.artists:
            songsOfX = self.artists[x]
            return songsOfX

    def searchForSong(self, x):
        if x in self.songs:
            song = self.songs[x]
            bandName = song[0]
            dates = song[1]
            return bandName, dates

    def topSongs(self, number):
        topSongs = []
        for i in self.songs:
            numOfListening = len(self.songs[i][1])
            while len(topSongs) <= numOfListening:
                topSongs.append([len(topSongs)])
            topSongs[numOfListening].append(i)

        index = 0
        length = len(topSongs)
        for i in range(length):
            if len(topSongs[index]) == 1:
                del topSongs[index]
                index -= 1
            index += 1

        return topSongs[-number:]

    def topArtist(self, number):
        topArtists = []
        for i in self.artists:
            numOfListening = 0
            for q in self.artists[i]:
                numOfListening += len(self.artists[i][q])
            while len(topArtists) <= numOfListening:
                topArtists.append([len(topArtists)])
            topArtists[numOfListening].append(i)

        index = 0
        length = len(topArtists)
        for i in range(length):
            if len(topArtists[index]) == 1:
                del topArtists[index]
                index -= 1
            index += 1

        return topArtists[-number:]

    def listInfo(self):
        for i in self.artists:
            print i
            for q in self.artists[i]:
                print "\t", q
                for k in self.artists[i][q]:
                    print "\t\t", k
            print

class Artist():
    def __init__(self, name):
        self.getLink(name)

    def getLink(self, artistName):
        self.linkOfArtist ="https://www.last.fm/music/"
        for i in artistName.split():
            self.linkOfArtist += i
            self.linkOfArtist += "+"
        self.linkOfArtist = self.linkOfArtist[:-1]

    def getGenres(self):
        try:
            page = requests.get(self.linkOfArtist)
        except requests.exceptions.ConnectionError, e:
            print e
        tree = html.fromstring(page.content)
        self.genres = tree.xpath("//ul[@class = 'tags-list tags-list--global']/li/a/text()")

    def getWiki(self):
        try:
            page = requests.get(self.linkOfArtist)
        except requests.exceptions.ConnectionError, e:
            print e
        tree = html.fromstring(page.content)
        self.shortWiki = tree.xpath("//div[@class = 'wiki-content']/p/text()")[0]

Okan = UserListerner("Lacin98")
#Lacin = UserListerner("Lacin98")
#Serkan = UserListerner("osteosit")

for i in Okan.topArtist(5):
    for q in range(1, len(i)):
        print i[0], "times", i[q]
        obj = Artist(i[q])
        obj.getGenres()
        for k in obj.genres:
            print "\t", k
