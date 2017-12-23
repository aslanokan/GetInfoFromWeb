from lxml import html
import requests

page = requests.get("https://eksisozluk.com")
tree = html.fromstring(page.content)
lis = []

trendTopics = tree.xpath("//div/div/nav/ul/li/a/text()")
countOfTrendTopics = tree.xpath("//div/div/nav/ul/li/a/small/text()")

for i in range(len(trendTopics)):
    lis.append([int(countOfTrendTopics[i]), trendTopics[i]])

for q in range(len(lis)):
    for j in range(q):
        if lis[q-j][0] < lis[q-j-1][0]:
            temp = lis[q-j]
            lis[q-j] = lis[q-j-1]
            lis[q-j-1] = temp

for k in reversed(lis):
    print str(k[0]) + (4-len(str(k[0])))*" " + k[1]
