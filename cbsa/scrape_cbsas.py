#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 
# Census Reporter geoids for CBSAs are of the form 31000USXXXXX
# where XXXXX is the 5-digit CBSA FIPS code. CBSA FIPS codes are unique among the combined set of 
# Metropolitan and Micropolitan statistical areas.
# 
# Geoids for Combined Statistical Areas (CSA) are of the form 33000USXXX
# where XXX is the 3-digit CSA FIPS code.
#
# The OMB also has a concept of "primary statistical area," which is an area that is not part of any # more extensive defined metropolitan area. All CSAs are primary statistical areas, as are CBSAs which
# are not combined into any other CSA.
# http://en.wikipedia.org/wiki/List_of_primary_statistical_areas_of_the_United_States

import unicodecsv
import statestyle
from lxml.html import fromstring
from urlparse import urljoin
from urllib import quote_plus
import re
import os.path

CBSA_OUTPUT_FILE = "../output/cbsas_with_links.csv"
CSA_OUTPUT_FILE = "../output/csas_with_links.csv"

WP_CBSA_LIST = 'http://en.wikipedia.org/wiki/List_of_Core_Based_Statistical_Areas'

from scrapelib import Scraper, FileCache, HTTPError

def parse_cbsa_codes():
    cbsas = {}
    csas = {}

    r = unicodecsv.reader(open("cbsa.csv"))
    h = r.next()
    for row in r:
        cbsa_code, metdiv_code, csa_code, cbsa_title, cbsa_type, metdiv_title, csa_title, county_name, state, fips_state, fips_county, central_or_outlying = row
        cbsas[cbsa_code] = { 'name': cbsa_title, 'link': None, 'csa': csa_code }
        if csa_code:
            csas[csa_code] = {'name': csa_title, 'link': None}

    return cbsas, csas

# would like to follow robots, but think that the robots parser is broken...
s = Scraper(requests_per_minute=90, follow_robots=False)
s.cache_storage = FileCache('../wikipedia_cache')
s.cache_write_only = False

def parse_cbsa_row(tr):
    cells = tr.findall('td')
    # rank, name, pop2012, pop2010, change, csa
    a = cells[1].find('a')
    cbsa_name = a.text[:-30].strip()
    cbsa_link = urljoin(WP_CBSA_LIST,a.attrib['href'])

    csa_name = csa_link = ''
    csa_anchor = cells[5].find('a')
    try:
        csa_name = csa_anchor.text[:-26].strip()
        csa_link = urljoin(WP_CBSA_LIST,csa_anchor.attrib['href'])
    except:
        pass

    return (cbsa_name, cbsa_link, csa_name, csa_link)


def wp_cbsa_reader():
    html = s.urlopen(WP_CBSA_LIST)
    doc = fromstring(html)
    cbsa_table = doc.findall('.//table')[1]
    pr_table =  doc.findall('.//table')[2]
    for tr in cbsa_table.findall('tr')[1:]:
        yield parse_cbsa_row(tr)

    for tr in pr_table.findall('tr')[1:]:
        yield parse_cbsa_row(tr)

def process_cbsas():
    cbsas, csas = parse_cbsa_codes()
    cbsa_by_name = dict((v['name'],k) for k,v in cbsas.items())
    csa_by_name =  dict((v['name'],k) for k,v in csas.items())

    for cbsa_name, cbsa_link, csa_name, csa_link in wp_cbsa_reader():
        try:
            cbsa_name = cbsa_name.replace(u'–','--')
            cbsa = cbsa_by_name[cbsa_name]
            cbsas[cbsa]['link'] = cbsa_link
            if cbsas[cbsa]['csa']:
                csas[cbsas[cbsa]['csa']]['link'] = csa_link

        except KeyError:
            print "Can't find CBSA ", cbsa_name

    return cbsas, csas

if __name__ == '__main__':
    cbsas, csas = process_cbsas()
    CBSA_HEADER = ['geoid','name','link','csa']
    w = unicodecsv.DictWriter(open(CBSA_OUTPUT_FILE,"wb"),fieldnames=CBSA_HEADER)
    w.writerow(dict(zip(CBSA_HEADER,CBSA_HEADER)))
    for k,v in cbsas.items():
        v['geoid'] = '31000US%s' % k
        w.writerow(v)

    CSA_HEADER = ['geoid','name','link']
    w = unicodecsv.DictWriter(open(CSA_OUTPUT_FILE,"wb"),fieldnames=CSA_HEADER)
    w.writerow(dict(zip(CSA_HEADER,CSA_HEADER)))
    for k,v in csas.items():
        v['geoid'] = '33000US%s' % k
        w.writerow(v)

