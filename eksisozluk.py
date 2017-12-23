from lxml import html
import requests
import webbrowser



lis = []
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


searchForTopics("https://eksisozluk.com/basliklar/gundem?p=1")
searchForTopics("https://eksisozluk.com/basliklar/gundem?p=2")
searchForTopics("https://eksisozluk.com/basliklar/gundem?p=3")

for q in range(len(lis)):
    for j in range(q):
        if lis[q-j][0] < lis[q-j-1][0]:
            temp = lis[q-j]
            lis[q-j] = lis[q-j-1]
            lis[q-j-1] = temp

for k in reversed(lis):
    print str(k[0]) + (4-len(str(k[0])))*" " + k[1]

def siteAdres(userInput):
    for i in lis:
        if i[1] == userInput+" ":
            return i[2]
