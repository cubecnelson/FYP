from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
import math
import re
from itertools import islice
import operator

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

db = MongoClient().test_database

data = {}

QUERY = 'nyc'

for tweet in db.tweets.find():
	for hashtag in tweet["entities"]["hashtags"]:
		hashtext = hashtag["text"].lower();
		try:
			data[hashtext] = data[hashtext] + 1
		except KeyError:
			data[hashtext] = 1
	
	#except KeyError, UnicodeEncodeError:
	#	print "Error"
temp = take(10, sorted(data.items(), key=operator.itemgetter(1), reverse=True))
top_10 = {}
for t in temp:
	top_10[t[0]] = t[1]
x = range(10)
plt.xticks(x, top_10.keys())
plt.scatter(x, top_10.values())
plt.show()