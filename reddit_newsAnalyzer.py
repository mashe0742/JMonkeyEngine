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
#nltk.download('vader_lexicon')
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
stop_words = stopwords.words("english")
import praw

#function for tokenization and cleaning of headlines
def process_text(headlines):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = []
    for line in headlines:
        toks = tokenizer.tokenize(line)
        toks = [t.lower() for t in toks if t.lower() not in stop_words]
        tokens.extend(toks)
    
    return tokens

#connect to reddit API using PRAW
reddit = praw.Reddit(client_id='CLIENT ID',
                     client_secret='CLIENT PRIVATE',
                     user_agent='USERNAME')

#actual connection to defined subreddit, retrieve 1000 new posts
headlines = set()

for submission in reddit.subreddit('politics').new(limit=None):
    headlines.add(submission.title)
    print(len(headlines))

#set up sentiment analyzer
sia = SIA()
results = []

#analyze headlines
for line in headlines:
    pol_score = sia.polarity_scores(line)
    pol_score['headline'] = line
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

print(df2.label.value_counts(normalize=True)*100)

#plot bar graph of results from sentiment analysis - Pos, Neut, Neg
fig, ax = plt.subplots()
counts = df.label.value_counts(normalize = True) * 100
sns.barplot(x=counts.index, y=counts, ax=ax)
#formatting of chart
ax.set_title("Distribution of /r/politics Headlines (% of whole)")
ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
ax.set_ylabel("Percentage")

plt.show()

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
plt.show()

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
plt.show()

#Analyze negative headlines, word distributions
neg_lines = list(df2[df2.label == -1].headline)

neg_tokens = process_text(neg_lines)
neg_freq = nltk.FreqDist(neg_tokens)

print(neg_freq.most_common(20))

#generate plots for distribution of negative words
y_val = [x[1] for x in neg_freq.most_common()]

fig = plt.figure(figsize=(10,5))
plt.plot(y_val)

plt.xlabel("words")
plt.ylabel("Frequency")
plt.title("Word Frequency Distribution (Negative)")
plt.show()

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
plt.show()