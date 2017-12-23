from lxml import html
import requests

page = requests.get("https://eksisozluk.com")
tree = html.fromstring(page.content)

trendTopics = tree.xpath("//div/div/nav/ul/li/a/text()")

for i in trendTopics:
    print i
