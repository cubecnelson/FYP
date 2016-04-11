from pymongo import MongoClient
from pattern.en import sentiment
import numpy as np
import matplotlib.pyplot as plt
import math
from math import sqrt
import re

db = MongoClient().test_database

data = []

QUERY = 'job'

def mean(lst):
    """calculates mean"""
    return sum(lst) / len(lst)

def stddev(lst):
    """returns the standard deviation of lst"""
    mn = mean(lst)
    variance = sum([(e-mn)**2 for e in lst])
    return sqrt(variance)

for tweet in db.tweets.find():
	myText = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet["text"].replace("#", "").replace("@", ""))
	#print tweet["favorite_count"]
	response = math.ceil(sentiment(myText.replace("#", ""))[0]*1000)/1000
	if response != 0.0:
		for hashtag in tweet["entities"]["hashtags"]:
			#print hashtag['text'].encode("utf-8")
			if QUERY.lower() in hashtag['text'].lower():
				data.append(response)
				break
			elif QUERY.lower() in tweet['text'].lower():
				data.append(response)
				break

	
	#except KeyError, UnicodeEncodeError:
	#	print "Error"
print "SD: " + stddev(data) + " " + "MEAN: " + mean(data)