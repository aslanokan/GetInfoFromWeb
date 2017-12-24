# -*- coding: utf-8 -*-

from lxml import html
import requests
import webbrowser



lis = []
lis2 = []
topics = []

def searchForTopics(link):
    try:
        page = requests.get(link)
    except requests.exceptions.ConnectionError, e:
        print e

    tree = html.fromstring(page.content)


    trendTopics = tree.xpath("//div/div/section/ul/li/a/text()")
    countOfTrendTopics = tree.xpath("//div/div/section/ul/li/a/small/text()")
    links = tree.xpath("//div/div/section/ul/li/a/@href")

    for i in range(len(trendTopics)):
        if(trendTopics[i] not in topics):
            lis.append([int(countOfTrendTopics[i]), trendTopics[i], links[i]])
            topics.append(trendTopics[i])


def searchForWriter(link):
    page = requests.get(link)
    tree = html.fromstring(page.content)

    writer = tree.xpath("//footer/div/a[@class='entry-date permalink']/text()")
    date = tree.xpath("//footer/div/a[@class='entry-author']/text()")
    entryNumber = tree.xpath("//footer/div/a[@class='entry-date permalink']/@href")

    for i in range(len(writer)):
        lis2.append([writer[i], date[i], "https://eksisozluk.com" + entryNumber[i]])


def searchForEntry(link):
    entry = ""
    page = requests.get(link)
    tree = html.fromstring(page.content)

    text = tree.xpath("//div[@class='content']/text() | //div[@class='content']/*/text()")
    for i in text:
        entry += " " + i

    return entry[6:]


def siteAdres(link):
    page = requests.get(link)
    tree = html.fromstring(page.content)

    text1 = tree.xpath("//div[@id='topic']/div/text()")
    text2 = tree.xpath("//div[@id='topic']/p/text()")

    if len(text1) >= 3:
        if text1[2][10:-9] == "böyle bir şey yok".decode('utf-8'):
            return False
    if text2 != []:
        if text2[0][:15] == "bu mümkün değil".decode('utf-8'):
            return False
    else:
        return link

def sortList():
    for q in range(len(lis)):
        for j in range(q):
            if lis[q-j][0] < lis[q-j-1][0]:
                temp = lis[q-j]
                lis[q-j] = lis[q-j-1]
                lis[q-j-1] = temp

def searchAndPrintTopics():
    searchForTopics("https://eksisozluk.com/basliklar/gundem?p=1")
    searchForTopics("https://eksisozluk.com/basliklar/gundem?p=2")
    searchForTopics("https://eksisozluk.com/basliklar/gundem?p=3")

    sortList()

    for k in reversed(lis):
        print str(k[0]) + (4-len(str(k[0])))*" " + k[1]

    del lis[:]
    del topics[:]

def getTopicLink(topic):
    link = link = "https://eksisozluk.com/" + topic
    page = requests.get(link)
    tree = html.fromstring(page.content)

    text = tree.xpath("//div[@id='topic']/h1/a/@href")
    return "https://eksisozluk.com" + text[0]

def readEntries(link, pageNumber):
    link = getTopicLink(topic) + "?p=" + str(pageNumber)
    if((siteAdres(link)) != False):
        searchForWriter(link)
        print "\n\n\n"
        for i in lis2:
            print i[0], i[1], "\n" ,searchForEntry(i[2])
    else:
        print "Try again"

def readAllEntries(topic, summary=False):
    page = 1
    link = getTopicLink(topic)
    while((siteAdres(link)) != False):
        searchForWriter(link)
        print "\n\n\n Page " + str(page) + ":"
        for i in lis2:
            if summary == True:
                print i[0], i[1], "\n" ,searchForEntry(i[2])[:50], "\n"
            else:
                print i[0], i[1], "\n" ,searchForEntry(i[2]), "\n"
        page += 1
        link = getTopicLink(topic) + "?p=" + str(page)
        del lis2[:]
    print "Done!!"


searchAndPrintTopics()

#pageNumber = int(raw_input("Page Number: "))
while(True):
    #readEntries(nextTopic, pageNumber)
    nextTopic = raw_input("Topic: ").decode('utf-8')
    if nextTopic == "":
        break
    elif nextTopic == "l":
        searchAndPrintTopics()
    else:
        if nextTopic[:3] == "-s ":
            readAllEntries(nextTopic[3:], True)
        else:
            readAllEntries(nextTopic)

    #pageNumber = int(raw_input("Page Number: "))
