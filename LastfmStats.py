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

info = getInfo("https://www.last.fm/user/Filojiston/library")
for i in info:
    for q in i:
        print q
    print
