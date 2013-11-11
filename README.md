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

