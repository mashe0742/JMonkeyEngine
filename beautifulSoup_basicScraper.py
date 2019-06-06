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

#parse html response looking for Reuters article tag, then save off all headlines
tags = soup.find_all('article')
for tag in tags:
    #drop time stamps, unwanted header lines
    if not any(value in tag.text for value in ("pm EDT", "h ago", "m ago", "Editor's Choice", "SUSTAINABLE BUSINESS", "SECTORS UP CLOSE")):
        print(tag.text.strip())