# -*- coding: utf-8 -*-

from lxml import html
import requests



def getMainNews():
    link = "http://www.diken.com.tr"
    try:
        page = requests.get(link)
    except requests.exceptions.ConnectionError, e:
        print e

    tree = html.fromstring(page.content)
    mainNews = tree.xpath("//div[@class='slide-excerpt-border ']/h2/a/text()")
    mainNewsLinks = tree.xpath("//div[@class='slide-excerpt-border ']/h2/a/@href")

    return (mainNews, mainNewsLinks)

def getNewsInfo(news):
    link = news
    try:
        page = requests.get(link)
    except requests.exceptions.ConnectionError, e:
        print e

    tree = html.fromstring(page.content)
    header = tree.xpath("//header[@class='entry-header']/h1/text()")
    enryTime = tree.xpath("//time[@class='entry-time']/text()")
    newsInfo = tree.xpath("//main[@class='content']/article/div[@class='entry-content']/p/text() | //main[@class='content']/article/div[@class='entry-content']/p/*/text()")

    return (header, enryTime, newsInfo)

for i in getMainNews()[1]:
    print getNewsInfo(i)[0][0]
    print ""
    for q in getNewsInfo(i)[2]:
        print q,
    print "\n\n\n\n\n"
