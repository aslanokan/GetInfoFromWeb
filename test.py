# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

url_to_scrape = 'http://apps2.polkcountyiowa.gov/inmatesontheweb/'

r = requests.get(url_to_scrape)

soup = BeautifulSoup(r.text)

inmates_links = []

for table_row in soup.select(".inmatesList tr"):
	table_cells = table_row.findAll('td')

	if len(table_cells) > 0:
		relative_link_to_inmate_details = table_cells[0].find('a')['href']
		absolute_link_to_inmate_details = url_to_scrape + relative_link_to_inmate_details
		inmates_links.append(absolute_link_to_inmate_details)
