"""
Experimenting with BeautifulSoup to pull data from reuters,
then search for and return all frontpage headlines

pulled headlines will be run through limited analysis using nltk

Written by Michael Ashe
"""

#libraries
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from bs4 import BeautifulSoup
import re
#nltk processing dependencies
import nltk
nltk.download('popular')
from nltk.corpus import stopwords
stop_words=set(stopwords.words("english"))
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
#from sklearn.linear_model import LogisticRegression, SGDCLassifier
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

#variable for url of page and dictionary to store headlines
target_page = 'https://www.reuters.com/'
headlinesDict = {}

#headers to pass useragent in order to evade bot detection
req = urllib2.Request(target_page, None, {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
response = urllib2.urlopen(req).read()

#query target page and return html var
#then use beautifulsoup parser to read page
page = response
soup = BeautifulSoup(page, 'html.parser')

#parse html response looking for Reuters article tag, then save off all headlines
tags = soup.find_all('article')
row = 0
for tag in tags:
    #drop time stamps, unwanted header lines
    if not any(value in tag.text for value in ("pm EDT", "h ago", "m ago", "Editor's Choice", "SUSTAINABLE BUSINESS", "SECTORS UP CLOSE")):
        headline = re.sub('(\n){2,}', ' ', tag.text.strip())
        if not any (value in headline for value in ("\n")):
            headlinesDict[row]=headline
            row+=1
        
#formatting to test output from json object to ensure sanitation of text
print("Headlines Retrieved:\n")
count=0

#sanitation to remove artifacts of scrape
headlinesDictCleaned = {k: v for k, v in headlinesDict.items() if v is not None}

#begin processing of text for use with nltk analysis
for element in headlinesDict:
    try:
        print('headline %s: %s' %(count,headlinesDictCleaned[count]))
        #tokenize each headline into sentences, then words
        tokenized_word = [word for sent in sent_tokenize(headlinesDictCleaned[count]) for word in word_tokenize(sent)]
        filtered_tokens = []
        for w in tokenized_word:
            if w not in stop_words:
                filtered_tokens.append(w)
        print(filtered_tokens)
        count+=1
    except:
        print('Exception!')
        count+=1
        continue
    
    
