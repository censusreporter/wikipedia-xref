#!/usr/bin/env python

import unicodecsv
import statestyle
import re
from lxml.html import fromstring
from urlparse import urljoin


from scrapelib import Scraper, FileCache

s = Scraper(requests_per_minute=60, follow_robots=False)
s.cache_storage = FileCache('wikipedia_cache')
s.cache_write_only = False

CD_LIST = 'https://en.wikipedia.org/wiki/List_of_United_States_congressional_districts'
OUTLIERS = ['District of Columbia', 'Puerto Rico']

def get_cd_page():
	writer = unicodecsv.writer(open('cd_wiki_data.csv', 'w'))
	writer.writerow(['full_geoid', 'wiki_url'])
	response = s.urlopen(CD_LIST)
	doc = fromstring(response)
	table = doc.find_class('wikitable')[0]
	for row in table.findall('tr')[1:]:
		geoid, url = parse_district(row[2])
		writer.writerow([geoid, url])

def parse_district(td):
	url = parse_url(td)
	text = td.text_content()
	state_regex = re.search("(?<!=\\d)\\D+", text)
	state = state_regex.group()
	if 'At-large' in text:
		state = re.sub(" At-large", "", state)
		cd_num = 0
	else:
		cd_regex = re.search("(\\b\\d+)", text)
		cd_num = cd_regex.group()
	if 'Incorrect' in text:
		stateobj = statestyle.get('California')
		cd_num = 8
		url = "https://en.wikipedia.org/wiki/California%27s_8th_congressional_district"
	else:
		stateobj = statestyle.get(state)
	if stateobj.name in OUTLIERS:
		cd_num = 98
	geoid = str(stateobj.fips).zfill(2) + str(cd_num).zfill(2)
	print geoid + ',' + url
	return (geoid, url)

def parse_url(td):
	a = td.find('a')
	href = a.attrib['href']
	url = urljoin(CD_LIST,href)
	return url

get_cd_page()


