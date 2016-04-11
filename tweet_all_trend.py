import time
import re
from trend import Trend
import json
from pymongo import MongoClient
import pymongo
from itertools import islice
import operator
import math
import getopt


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

db = MongoClient().test_database

n = 0.0
QUERY = 'ROOT'

first = Trend()
first.setName(QUERY)
for tweet in db.tweets.find():
	for hashtag in tweet["entities"]["hashtags"]:
		if hashtag['text'].encode("utf-8").lower() != QUERY.lower():
			first.addToRelated(hashtag['text'].encode("utf-8").lower(),1)
	n = n + 1

print QUERY.lower(), ": ", str(n)
top_10 = sorted(first.getRelated().items(), key=operator.itemgetter(1), reverse=True)

for top in top_10:
	print "\t", top[0], ": ", float(top[1])/n 

print len(top_10)
first.clear()