# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 12:52:34 2019

@author: Michael
"""
import requests
import json
import datetime
import os
import csv

#storage variables for subreddit data mining
subStats = {}
sub = 'The_Donald'
before = "1560038399"
after = "1554076800" 
query = ""
subCount = 0

#connect to reddit API using pushshift
#note that before and after date must be in epoch time
def getPushShiftData(query, after, before, sub):
    if not query:
        url= 'https://api.pushshift.io/reddit/search/submission/?after=%s&size=1000&before=%s&subreddit=%s' % (after, before, sub)
    else:
        url= 'https://api.pushshift.io/reddit/search/submission/?q=%s&after=%s&size=1000&before=%s&subreddit=%s' % (query, after, before, sub)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']
#extraction functions
def collectSubData(subm):
    subData = list() #list for storing all points of data
    title = subm['title']
    url = subm['url']
    try:
        flair = subm['link_flair_text']
    except KeyError:
        flair = "NaN"
    author = subm['author']
    sub_id = subm['id']
    score = subm['score']
    created = datetime.datetime.fromtimestamp(subm['created_utc'])
    numComms = subm['num_comments']
    permalink = subm['permalink']
    
    subData.append((sub_id,title,url,author,score,created,numComms,permalink,flair))
    subStats[sub_id] = subData
#function to save off data to csv
def updateSubs_file():
    uploadCount = 0
    location = "Reddit_Data"
    if not os.path.exists(location):
        os.mkdir(location)
    print("input filename")
    filename = input() + '.csv'
    file = location + "\\" +filename
    with open(file,'w',newline="",encoding='utf-8') as file:
        a=csv.writer(file, delimiter=',')
        headers=["Post ID","Title","URL","Author","Score","Published","Total Comments","Permalink","Flair"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            uploadCount+=1
        print(str(uploadCount)+" submissions have been saved to file")
        file.close()

data = getPushShiftData(query, after, before, sub)
#Loop until all posts have been gathered from target time range
#TODO: find out why I can only get 25 results. JSON error is caused by metadata 
#at position 26
try:
    while len(data) > 0:
        for submission in data:
            collectSubData(submission)
            subCount+=1
        #call getPushShiftData() with the created dat of the last submission
        print(len(data))
        print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
        after = data[-1]['created_utc']
        data = getPushShiftData(query,after,before,sub)
        
    print(len(data))

except json.decoder.JSONDecodeError:
    print("JSON End")

file = updateSubs_file()