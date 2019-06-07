"""
Created on Fri Jun  7 16:12:09 2019

@author: Michael Ashe, modified code from Brendan Martin and Nikos Koufos at
LearnDataSci
"""

import math
import random
from collections import defaultdict
from pprint import pprint
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from imblearn.over_sampling import SMOTE
#prevent deprecation warnings in output
import warnings
warnings.filterwarnings(action='ignore')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#set global plot style
sns.set_style(style="white")
sns.set_context(context='notebook', font_scale=1.3, rc={'figure.figsize':(16,9)})

#read in csv file taken from news classifier
df = pd.read_csv('reddit_headline_labels.csv', encoding='utf-8')

df = df[df.label != 0]
counts = df.label.value_counts()

sm = SMOTE()

#measure predicted accuracy
print("\nPredicting only -1 = {:.2f}% accuracy.".format(counts[-1] / sum(counts) * 100))

#transform the headlines into vectors, prepare training data
X = df.headline
y = df.label

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

#begin training
vect = CountVectorizer(max_features=1000, binary=True)

X_train_vect = vect.fit_transform(X_train)

#perform SMOTE balancing to improve training data
X_train_res, y_train_res = sm.fit_sample(X_train_vect, y_train)

unique, counts = np.unique(y_train_res, return_counts=True)

#load training data and score for fit
nb = MultinomialNB()
nb.fit(X_train_res, y_train_res)
#print(nb.score(X_train_res, y_train_res))

#make predictions of test data and store them in y_pred
X_test_vect = vect.transform(X_test)
y_pred = nb.predict(X_test_vect)

#calculate accuracy metrics
print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
print("\nF1 Score: {:.2f}".format(f1_score(y_test, y_pred) * 100))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))