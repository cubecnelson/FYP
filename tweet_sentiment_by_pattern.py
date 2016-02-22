from pymongo import MongoClient
from pattern.en import sentiment
import numpy as np
import matplotlib.pyplot as plt
import math
import re

db = MongoClient().test_database

data = {}

QUERY = 'newyork'

for tweet in db.tweets.find():
	myText = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet["text"].replace("#", "").replace("@", ""))
	#print tweet["favorite_count"]
	response = math.ceil(sentiment(myText.replace("#", ""))[0]*20)/20
	if response != 0.0:
		for hashtag in tweet["entities"]["hashtags"]:
			#print hashtag['text'].encode("utf-8")
			if QUERY.lower() in hashtag['text'].lower():
				try:
					data[response] = data[response] + 1
				except KeyError:
					data[response] = 1
			elif QUERY.lower() in tweet['text'].lower():
				try:
					data[response] = data[response] + 1
				except KeyError:
					data[response] = 1
				break

	
	#except KeyError, UnicodeEncodeError:
	#	print "Error"
plt.title("\"" + QUERY.upper() + "\""  + ": SENTIMENT - #TWEETS")
plt.scatter(data.keys(), data.values())
plt.show()