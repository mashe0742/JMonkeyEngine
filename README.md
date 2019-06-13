# Reddit Scraper
------
## beautifulSoup_basicScraper
### Experiment with BeautifulSoup to write a parser that will take headlines from the front page of Reuters and then create a word cloud from them.

### TODO:
- fix handling of special sections (currently do not appear or have excessive whitespace due to formatting issues)
- implemenation of word cloud processor
	- output of word cloud for potential follow-on processing
------
## reddit_newsAnalyzer
### Experiment using NLTK and the PRAW Reddit API in order to analyze sentiment of top 1000 posts from an arbitrary subreddit

### TODO:
- Automatic report generation
- Implement word cloud for top words from negative and positive set
------
## reddit_bayes_textClassifier
### follow-on to news analyzer that uses naive bayes algorithm to attempt to classify posts from subreddit and then predict sentiment of test data

### TODO:
- Improve accuracy of model
- Increase training data set
- Implement GPU acceleration
------
Text classifier scripts made by following and modifying tutorials from https://www.learndatasci.com/tutorials
