"""
Clone of Reuters scraper to take headlines instead from Reddit
and analyze sentiment, in order to explore differences in 
headlines written by mainstream news source vs headlines displayed on 
Reddit.

@author: Michael Ashe
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
#nltk.download('vader_lexicon')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
stop_words = stopwords.words("english")

#function for tokenization and cleaning of headlines
def process_text(headlines):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = []
    for line in headlines:
        toks = tokenizer.tokenize(line)
        toks = [t.lower() for t in toks if t.lower() not in stop_words]
        tokens.extend(toks)
    
    return tokens

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

print(soup)
#parse html response looking for Reuters article tag, then save off all headlines
tags = soup.find_all('article')

print(tags)

row = 0
for tag in tags:
    #drop time stamps, unwanted header lines
    if not any(value in tag.text for value in ("pm EDT", "h ago", "m ago", "Editor's Choice", "SUSTAINABLE BUSINESS", "SECTORS UP CLOSE")):
        headline = re.sub('(\n){2,}', ' ', tag.text.strip())
        if not any (value in headline for value in ("\n")):
            headlinesDict[row]=headline
            row+=1


#sanitation to remove artifacts of scrape
headlinesDictCleaned = {k: v for k, v in headlinesDict.items() if v is not None}

#set up sentiment analyzer
sia = SIA()
results = []

#analyze headlines
for key, value in headlinesDictCleaned.items():
    pol_score = sia.polarity_scores(value)
    pol_score['headline'] = value
    results.append(pol_score)

#push to pandas
df = pd.DataFrame.from_records(results)
df['label'] = 0
#label data as positive, neutral, or negative based on compound score
df.loc[df['compound'] > 0.2, 'label'] = 1
df.loc[df['compound'] < -0.2, 'label'] = -1

#save to csv file
df2 = df[['headline', 'label']]
#df2.to_csv('reuters_headline_labels.csv', mode='a',encoding='utf-8',index=False)
print(df2.label.value_counts)
print(df2.label.value_counts(normalize=True)*100)

#plot bar graph of results from sentiment analysis - Pos, Neut, Neg
fig, ax = plt.subplots()
counts = df.label.value_counts(normalize = True) * 100
sns.barplot(x=counts.index, y=counts, ax=ax)
#formatting of chart
ax.set_title("Distribution of Reuters Headlines (% of whole)")
ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
ax.set_ylabel("Percentage")

plt.show()

#tokenize sentences and perform follow-on analysis
pos_lines = list(df2[df2.label == 1].headline)

print(pos_lines)

pos_tokens = process_text(pos_lines)
pos_freq = nltk.FreqDist(pos_tokens)

print(pos_freq.most_common(20))

#plot frequency distribution to discern patterns from words
y_val = [x[1] for x in pos_freq.most_common()]

fig = plt.figure(figsize=(10,5))
plt.plot(y_val)

plt.xlabel("Words")
plt.ylabel("Frequency")
plt.title("Word Frequency Distribution (Positive)")
plt.show()