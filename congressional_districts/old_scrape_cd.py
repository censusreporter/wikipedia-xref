#!/usr/bin/env python

import unicodecsv
import statestyle
import re
from lxml.html import fromstring
from urlparse import urljoin

# I copied this code from scrape_states.py

from scrapelib import Scraper, FileCache

s = Scraper(requests_per_minute=60, follow_robots=False)
s.cache_storage = FileCache('wikipedia_cache')
s.cache_write_only = False

# My Stuff

CD_LIST = 'https://en.wikipedia.org/wiki/List_of_United_States_congressional_districts'
NON_VOTING = ['American Samoa', 'District of Columbia', 'Guam', 'Northern Mariana Islands', 'Puerto Rico', 'United States Virgin Islands']
NOT_STATES = ['Philippines', 'U.S. Virgin Islands']

def parse_cd_file():
	writer = unicodecsv.writer(open('cd_wiki_data.csv', 'w'))
	writer.writerow(['full_geoid', 'wiki_url'])
	response = s.urlopen(CD_LIST)
	doc = fromstring(response)
	for h2 in doc.findall('.//h2')[2:59]:
		for span in h2.find_class('mw-headline'):
			if span.text_content() in NOT_STATES:
				break	
			state = statestyle.get(span.text_content())
			if state.name not in NON_VOTING:
				ul = span.getparent().getnext().getnext().getnext()
				print_output(state, ul)

def print_output(state, ul):
	for i,li in enumerate(ul.findall('li')):
		item = li.text_content()
		if 'obsolete' not in item:
			a = li.find('a')
			href = a.attrib['href']
			url = urljoin(CD_LIST,href)
			if 'At-large' in item:
				print state.fips + '00' + ',' + url
			else:
				x = re.search('((?<=_)\d+)', url)
				print str(state.fips).zfill(2) + x.group().zfill(2) + ',' + url

parse_cd_file()


# Problems
# 	Florida, Texas, Wyoming

