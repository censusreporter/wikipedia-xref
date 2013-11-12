#!/usr/bin/env python
# 
# Census Reporter geoids for counties are of the form 05000USXXYYY
# where XX is the 2-digit state FIPS code and YYY is the 3-digit county FIPS code. Together, these are unique nationwide.
# 
# 
import unicodecsv
import statestyle
from lxml.html import fromstring
from urlparse import urljoin
import re

from scrapelib import Scraper, FileCache
BASE_URL = 'https://en.wikipedia.org/wiki/'
STATE_LIST = 'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States'

# would like to follow robots, but think that the robots parser is broken...
s = Scraper(requests_per_minute=60, follow_robots=False)
s.cache_storage = FileCache('wikipedia_cache')
s.cache_write_only = False

def write_state_file():
    response = s.urlopen(STATE_LIST)
    doc = fromstring(response)
    table = doc.find_class('wikitable')[0]
    writer = unicodecsv.writer(open('state_wiki_data.csv', 'w'))
    writer.writerow(['full_geoid', 'wiki_url'])
    for row in table.findall('tr')[1:]:
        fips, url = parse_state_row(row)
        fips = '04000US' + fips
        writer.writerow([fips,url])
    writer.writerow('04000US72','https://en.wikipedia.org/wiki/Puerto_Rico')
    writer.writerow('04000US11','https://en.wikipedia.org/wiki/Washington,_D.C.')
    

def parse_state_row(row):
    tds = row.findall('td')
    postal = tds[0].text_content()
    state = statestyle.get(postal)
    ths = row.findall('th')
    a = ths[0].find('a')
    href = a.attrib['href']
    return (state.fips.zfill(2), urljoin(BASE_URL,href))

if __name__ == '__main__':
    write_state_file()

