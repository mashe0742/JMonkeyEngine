"""
Clone of Reuters scraper to take headlines instead from Reddit
and analyze sentiment, in order to explore differences in 
headlines written by mainstream news source vs headlines displayed on 
Reddit.

@author: Michael Ashe, modified code from Brendan Martin and Nikos Koufos at
LearnDataSci
"""

#libraries
#nltk processing dependencies
import nltk
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')
#nltk components
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
stop_words = stopwords.words("english")
import os

#function for tokenization and cleaning of headlines
def process_text(headlines):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = []
    for line in headlines:
        toks = tokenizer.tokenize(line)
        toks = [t.lower() for t in toks if t.lower() not in stop_words]
        tokens.extend(toks)
    
    return tokens

#read in data from csv, changing directory to where it was saved by reddit_dataRetrieval
os.chdir('Reddit_Data')
df = pd.read_csv('redditTestData.csv', encoding='utf-8')
titles = df['Title']
os.chdir('..')

#set up sentiment analyzer
sia = SIA()
results = []

#analyze headlines
entryCounter = 0
for entry in titles:
    print(entry)
    pol_score = sia.polarity_scores(entry)
    pol_score['headline'] = entry
    results.append(pol_score)
    entryCounter+=1

#push to pandas
df = pd.DataFrame.from_records(results)
df['label'] = 0
#label data as positive, neutral, or negative based on compound score
df.loc[df['compound'] > 0.2, 'label'] = 1
df.loc[df['compound'] < -0.2, 'label'] = -1

#save to csv file
df2 = df[['headline', 'label']]
#df2.to_csv('reddit_headline_labels.csv', mode='a',encoding='utf-8',index=False)

print(df2.label.value_counts(normalize=True)*100)

#plot bar graph of results from sentiment analysis - Pos, Neut, Neg
fig, ax = plt.subplots()
counts = df.label.value_counts(normalize = True) * 100
sns.barplot(x=counts.index, y=counts, ax=ax)
#formatting of chart
ax.set_title("Distribution of /r/the_donald Headlines (% of whole)")
ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
ax.set_ylabel("Percentage")
plt.savefig('plots/subreddit_sentiment_distribution.png')

#tokenize sentences and perform follow-on analysis
pos_lines = list(df2[df2.label == 1].headline)

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
plt.savefig('plots/positive_word_distribution.png')

#log-log plot to simplify interpretation of distribution data
y_final = []
for i, k, z, t in zip(y_val[0::4], y_val[1::4], y_val[2::4], y_val[3::4]):
    y_final.append(math.log(i+k+z+t))

x_val = [math.log(i+1) for i in range(len(y_final))]

fig = plt.figure(figsize=(10,5))

plt.xlabel("Words (Log)")
plt.ylabel("Frequency (Log)")
plt.title("Word Frequency Distribution, Log (Positive)")
plt.plot(x_val, y_final)
plt.savefig('plots/positive_word_distribution_log.png')

#Analyze negative headlines, word distributions
neg_lines = list(df2[df2.label == -1].headline)

neg_tokens = process_text(neg_lines)
neg_freq = nltk.FreqDist(neg_tokens)

print(neg_freq.most_common(20))

#generate plots for distribution of negative words
y_val = [x[1] for x in neg_freq.most_common()]

fig = plt.figure(figsize=(10,5))
plt.plot(y_val)

plt.xlabel("Words")
plt.ylabel("Frequency")
plt.title("Word Frequency Distribution (Negative)")
plt.savefig('plots/negative_word_distribution.png')

#generate log-log plot of negative word distribution
y_final = []
for i,k,z in zip(y_val[0::3], y_val[1::3], y_val[2::3]):
    if i+k+z ==0:
        break
    y_final.append(math.log(i+k+z))
    
x_val = [math.log(i+1) for i in range(len(y_final))]

fig = plt.figure(figsize=(10,5))

plt.xlabel("Words (Log)")
plt.ylabel("Frequency (Log)")
plt.title("Word Frequency Distribution, Log (Negative)")
plt.plot(x_val, y_final)
plt.savefig('plots/negative_word_distribution_log.png')