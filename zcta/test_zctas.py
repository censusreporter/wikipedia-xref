#!/usr/bin/env python
# 
# Census Reporter geoids for counties are of the form 06000USXXYYYYY
# where XX is the 2-digit state FIPS code and YYYYY is the 5-digit place FIPS code. Together, these are unique nationwide.
# 
# Wikipedia has no list of all census places, so the strategy here is to go through the Gazetteer (the official list of places)
# and attempt to find them on Wikipedia. This is done by constructing a potential page name from the place name and the state name.
# If the URL return a page, then an attempt is made to find the FIPS ID/geoid in the page. In the best case scenario, that is found
# and it matches the Gazetteer's geoid. 
#
# Because this is an indeterminate process, we expect to run this repeatedly. Therefore, taking advantage of scrapelib's caching and
# reading in what was output on the last run can make things more efficient.
#
import unicodecsv
from lxml.html import fromstring
from urlparse import urljoin
from urllib import quote_plus
import re
import os, os.path

OUTPUT_FILE = "zctas.csv"

from scrapelib import Scraper, FileCache, HTTPError
BASE_URL = 'https://en.wikipedia.org/wiki/'

# would like to follow robots, but think that the robots parser is broken...
s = Scraper(requests_per_minute=90, follow_robots=False)
s.cache_storage = FileCache('../wikipedia_cache')
s.cache_write_only = False

def test_zips():
    existing = {}
    if os.path.exists(OUTPUT_FILE):
        for row in unicodecsv.DictReader(open(OUTPUT_FILE)):
            existing[row['zip']] = row
        os.rename(OUTPUT_FILE,OUTPUT_FILE + '.bak')
    r = unicodecsv.DictReader(open("2013_Gaz_zcta_national.txt"),delimiter="\t")
    f = r.fieldnames
    writer = unicodecsv.DictWriter(open(OUTPUT_FILE,"w"),['zip','wiki_url'])
    writer.writerow({'zip': 'zip','wiki_url': 'wiki_url'})
    hits = misses = 0
    for count,row in enumerate(r):
        url = urljoin(BASE_URL,row['GEOID'])
        try:
            d = existing[row['GEOID']]
            hits += 1
        except:
            d = { 'zip': row['GEOID'], 'wiki_url': ''}
            try:
                doc = fromstring(s.urlopen(url))
                d['wiki_url'] = url
                hits += 1
            except:
                misses += 1 # we don't expect them all to hit
        writer.writerow(d)
        if count % 100 == 0: print count
    return hits, misses







    
if __name__ == '__main__':
    hits, misses = test_zips()
    print "Done"
    print "tried %i" % (hits + misses)
    print "%i hits" % hits
    print "%i misses" % misses
