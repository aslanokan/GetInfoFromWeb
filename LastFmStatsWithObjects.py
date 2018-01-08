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
        self.stopPage = 100

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
            topSongs[numOfListening].append([self.songs[i][0], i])


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
    def __init__(self, Artistname):
        self.getLink(Artistname)

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
        self.genresOfArtist = tree.xpath("//ul[@class = 'tags-list tags-list--global']/li/a/text()")

    def getWiki(self):
        try:
            page = requests.get(self.linkOfArtist)
        except requests.exceptions.ConnectionError, e:
            print e
        tree = html.fromstring(page.content)
        self.shortWiki = tree.xpath("//div[@class = 'wiki-content']/p/text()")[0]


class Song():
    def __init__(self, songInfo):
        self.songName = songInfo[1]
        self.artistName = songInfo[0]
        self.getLink(self.artistName, self.songName)

    def getLink(self, artistName, songName):
        self.linkOfSong ="https://www.last.fm/music/"
        for i in artistName.split():
            self.linkOfSong += i
            self.linkOfSong += "+"
        self.linkOfSong = self.linkOfSong[:-1]

        self.linkOfSong += "/_/"

        for i in songName.split():
            self.linkOfSong += i
            self.linkOfSong += "+"
        self.linkOfSong = self.linkOfSong[:-1]

    def getGenres(self):
        try:
            page = requests.get(self.linkOfSong)
        except requests.exceptions.ConnectionError, e:
            print e
        tree = html.fromstring(page.content)
        self.genresOfSong = tree.xpath("//ul[@class = 'tags-list tags-list--global']/li/a/text()")


Okan = UserListerner("Filojiston")
#Lacin = UserListerner("Lacin98")
#Serkan = UserListerner("osteosit")
Okan.listInfo()
while True:
    print Okan.searchForSong(raw_input(": "))

"""
for i in Okan.topSongs(3):
    for q in range(1, len(i)):
        print i[0], "times", i[q][0], "-", i[q][1]
        song = Song(i[q])
        song.getGenres()
        for k in song.genresOfSong:
            print "\t", k
    print
"""

"""
for i in Okan.topArtist(7):
    for q in range(1, len(i)):
        print i[0], "times", i[q]
        obj = Artist(i[q])
        obj.getGenres()
        for k in obj.genresOfArtist:
            print "\t", k
"""
