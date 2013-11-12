wikipedia-xref
==============

Code to develop a cross-reference between US Census Bureau geography identifiers and Wikipedia pages about those places.

Getting Started
===============
To work on scrapers for this project, you need to install some python libraries. You are strongly encouraged to use virtualenv. These instructions further assume that you've installed virtualenvwrapper.

```
mkvirtualenv wikipedia-xref
pip install -r requirements.txt
```

The End Goal
============
For [Census Reporter](http://censusreporter.org), we would like to have a solid cross-reference between Census geography identifiers and Wikipedia pages, so that we can provide easy links from our profile pages to a relevant Wikipedia page.

For each geography level, produce a datafile which has, at minimum, the full Census Reporter geoids and a single corresponding Wikipedia URL. The first row of the file should be column headers, and the headers for those two columns should be exactly "full_geoid" and "wiki_url" It is fine to have other columns in the output file if they are useful for visual checking or other reference. If you are producing the file from a comprehensive list of geoids for that geography level, it is ok to have blank values for wiki_url.

In many cases, the [official Census gazetteer files](http://www.census.gov/geo/maps-data/data/gazetteer2013.html) for various summary levels will be useful.

Status
======
## Done

* state 
* county - https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county-equivalents

## Work in Progress

* place - about 2/3 solid matches; Census Designated Places are likely to be challenging; many have related pages for townships/county subs. Currently saves constructed URLs even when 404 or not clearly matched. Need to decide our preferred confidence level and filter accordingly/consider what lengths to go to to find pages for CDPs and others that may have "equivalently" usable pages in WP that we just can't identify programmatically.

## To Be Assessed (all of the other tiger file types)
### more promising (cost/benefit)
* cbsa ([942](http://www.census.gov/geo/maps-data/data/tallies/national_geo_tallies.html)) Should be not too hard to do based on exact name matches from [WP list](https://en.wikipedia.org/wiki/List_of_Core_Based_Statistical_Areas)
* csa ([125](http://www.census.gov/geo/maps-data/data/tallies/national_geo_tallies.html)) - https://en.wikipedia.org/wiki/List_of_Combined_Statistical_Areas
* cd ([436](http://www.census.gov/geo/maps-data/data/tallies/national_geo_tallies.html)) https://en.wikipedia.org/wiki/List_of_Congressional_Districts - shouldn't be too complicated
* zcta5 - many ZIP codes redirect to neighborhood pages. May be worth just going through the Gazetteer and testing URLs kind of like with places

### less promising
* aiannh ([695](http://www.census.gov/geo/maps-data/data/tallies/national_geo_tallies.html)) (American Indian, Alaska Native, Native Hawaiian lands) some are in Wikipedia. Probably hard to do systematically. [Wikipedia list](https://en.wikipedia.org/wiki/List_of_Indian_reservations_in_the_United_States)
* aits ([492](http://www.census.gov/geo/maps-data/data/tallies/national_geo_tallies.html)) American Indian Tribal Subdivision
* anrc ([12](http://www.census.gov/geo/maps-data/data/tallies/national_geo_tallies.html)) [Alaska Native Regional Corporations](https://en.wikipedia.org/wiki/Alaska_Native_Regional_Corporations)
* cousub - County Subdivision, aka Township, etc. Many have Wikipedia pages. Some overlap with census designated places. Hard to know how to rigorously search for them.
* elsd - Elementary School Districts
* scsd - Secondary School Districts
* unsd - Unified School district
* sldl - State legislative district - lower chamber
* sldu - State legislative district - upper chamber

### Low likelihood of usable wikipedia pages
* tabblock - block
* tbg - tribal block group
* tract - tract
* ttract - tribal tract
* cnecta ([10](http://www.census.gov/geo/maps-data/data/tallies/national_geo_tallies.html)) - not sure if there's a good list.
* concity ([7](http://www.census.gov/geo/maps-data/data/tallies/national_geo_tallies.html)) - this [WP list](https://en.wikipedia.org/wiki/Consolidated_city-county#List_of_consolidated_city-counties) is longer than 7 
* necta - New England City and Town Areas
* nectadiv - NECTA divisions
* puma - Public Use Microdata Area
* uac - Urbanized Areas and Urban Clusters
* vtd - voting district
* metdiv - Metropolitan Divisions - 11 metropolitan areas are divided into 31 metropolitan divisions. There probably aren't good WP pages for these.
* submcd - sub minor civil division
