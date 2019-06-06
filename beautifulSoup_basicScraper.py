# -*- coding: utf-8 -*-
"""
Experimenting with BeautifulSoup to pull data from reuters,
then search for and return all frontpage headlines

- Michael Ashe
"""

#libraries
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import requests
from bs4 import BeautifulSoup

#variable for url of page
target_page = 'https://www.reuters.com/'

#headers to pass useragent in order to evade bot detection
req = urllib2.Request(target_page, None, {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
response = urllib2.urlopen(req).read()

#query target page and return html var
page = response

#use beautifulsoup parser to read page
soup = BeautifulSoup(page, 'html.parser')

print(soup)