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

COUNTY_LIST = 'https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county-equivalents'
# Municipalities in Puerto Rico are "county-equivalents"
PR_MUNICIPALITIES = 'https://en.wikipedia.org/wiki/Municipalities_of_Puerto_Rico'

# would like to follow robots, but think that the robots parser is broken...
s = Scraper(requests_per_minute=60, follow_robots=False)
s.cache_storage = FileCache('../wikipedia_cache')
s.cache_write_only = False


def parse_county_row(row):
    cells = row.findall('td')
    fips = cells[0].text_content()
    a = cells[1].find('a')
    href = a.attrib['href']
    return (fips, urljoin(BASE_URL,href))
    
def parse_municipalities_row(row):
    cells = row.findall('td')
    fips = cells[1].find_class('sorttext')[0].text_content()
    fips = '72' + fips
    a = cells[0].find('.//a')
    href = a.attrib['href']
    return (fips, urljoin(BASE_URL,href))
    
def make_wp_dict():
    d = {}

    # read US county list
    response = s.urlopen(COUNTY_LIST)
    doc = fromstring(response)
    table = doc.find_class('wikitable')[0]
    for row in table.findall('tr')[1:]:
        fips, url = parse_county_row(row)
        d[fips] = url

    # now do PR
    response = s.urlopen(PR_MUNICIPALITIES)
    doc = fromstring(response)
    table = doc.find_class('wikitable')[0]
    for row in table.findall('tr')[1:]:
        fips, url = parse_municipalities_row(row)
        d[fips] = url

    return d    

def produce_xref():
    in_reader = unicodecsv.DictReader(open("Gaz_counties_national.txt"),delimiter="\t", encoding='latin-1')
    fields = ['full_geoid','state','name','wiki_url']
    out_writer = unicodecsv.DictWriter(open("counties_with_links.csv","w"),fields, encoding='utf-8')
    out_writer.writerow(dict(zip(fields,fields)))

    wp_dict = make_wp_dict()
    for row in in_reader:
        d = {
            'full_geoid': '05000US' + row['GEOID'],
            'state': row['USPS'],
            'name': row['NAME'],
            'wiki_url': ''
        }
        try:
            d['wiki_url'] = wp_dict[row['GEOID']]
        except:
            print "%(NAME)s (%(GEOID)s) not found" % row
        out_writer.writerow(d)

if __name__ == '__main__':
    # maybe later we'll use CLI args for the output file name
    produce_xref()
    