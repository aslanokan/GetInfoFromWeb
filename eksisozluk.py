from lxml import html
import requests
import webbrowser



lis = []
lis2 = []
topics = []

def searchForTopics(link):
    page = requests.get(link)
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

    print entry[6:]


def siteAdres(userInput):
    for i in lis:
        if i[1] == userInput+" ":
            return "https://eksisozluk.com" + i[2][:-10]

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


searchAndPrintTopics()
nextTopic = raw_input(": ")
searchForWriter(siteAdres(nextTopic))

print "\n\n\n"
for i in lis2:
    print i[0], i[1], "\n" ,searchForEntry(i[2])
