from pymongo import MongoClient
from pattern.en import sentiment
import numpy as np
import matplotlib.pyplot as plt
import math
import re

db = MongoClient().test_database

count = 0.0
data = {}

QUERY = ''



for tweet in db.tweets.find():
	myText = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet["text"].replace("#", "").replace("@", ""))
	#print tweet["favorite_count"]
	response = math.ceil(sentiment(myText.replace("#", ""))[0]*20)/20
	if response != 0.0:
		for hashtag in tweet["entities"]["hashtags"]:
			#print hashtag['text'].encode("utf-8")
			if QUERY.lower() in hashtag['text'].lower():
				try:
					data[response] = data[response] + 1.0
				except KeyError:
					data[response] = 1.0
				count = count + 1.0
				break
			elif QUERY.lower() in tweet['text'].lower():
				try:
					data[response] = data[response] + 1.0
				except KeyError:
					data[response] = 1.0
				count = count + 1.0
				break

	
for key in data.keys():
	data[key] = data[key]/count


plt.title("\"" + QUERY.upper() + "\""  + ": SENTIMENT - #TWEETS")
plt.scatter(data.keys(), data.values())
plt.show()