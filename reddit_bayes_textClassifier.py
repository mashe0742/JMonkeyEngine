"""
Created on Fri Jun  7 16:12:09 2019

@author: Michael Ashe, modified code from Brendan Martin and Nikos Koufos at
LearnDataSci
"""

import math
import random
from collections import defaultdict
from pprint import pprint

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
print(df.label.value_counts())