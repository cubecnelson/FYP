import time
import re
from trend import Trend
import json
from pymongo import MongoClient
from itertools import islice
import operator
import math
import getopt


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

db = MongoClient().test_database

n = 0.0
QUERY = 'tv'

first = Trend()
first.setName(QUERY)
for tweet in db.tweets.find():
	trend_in_tweet = False
	for hashtag in tweet["entities"]["hashtags"]:
		trend_in_tweet = QUERY.lower() == hashtag['text'].lower()
		if trend_in_tweet == True:
			for hashtag in tweet["entities"]["hashtags"]:
				if hashtag['text'].encode("utf-8").lower() != QUERY:
					first.addToRelated(hashtag['text'].encode("utf-8").lower(),1)
	if trend_in_tweet == True:	
		n = n + 1

print QUERY, ": ", str(n)
top_10 = sorted(first.getRelated().items(), key=operator.itemgetter(1), reverse=True)
top_10 = take(10, top_10)
for top in top_10:
	print "\t", top[0], ": ", -math.log(float(top[1])/n) 
first.clear()