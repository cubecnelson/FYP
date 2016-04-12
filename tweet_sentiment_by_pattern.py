from pymongo import MongoClient
import pymongo
from pattern.en import sentiment
import numpy as np
import matplotlib.pyplot as plt
import math
import re

db = MongoClient().test_database

for trend in db.trends.find():
	count = 0.0
	
	data = {}

	print trend['_id']
	QUERY = trend['_id']

	QUERY = QUERY.lower()

	record = []

	zeros = np.linspace(-1,1,40)


	for zero in zeros:
		try:
			zero = math.ceil(zero*20)/20
			data[zero] = 0
		except KeyError:
			data[zero] = 0
			break


	#plt.show()
	for tweet in db.tweets.find({"entities.hashtags.text": re.compile(QUERY, re.IGNORECASE)}):
		myText = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet["text"].replace("#", "").replace("@", ""))
		#print tweet["favorite_count"]
		response = math.ceil(sentiment(myText.replace("#", ""))[0]*20)/20
		if response != 0.0:
				#print hashtag['text'].encode("utf-8")
			record.append(response)
			count = count + 1.0
			try:
				data[response] = data[response] + 1.0
			except KeyError:
				data[response] = 1.0
				
	print data
		
	if count != 0:
		for key in data.keys():
			data[key] = data[key]/count

	values = data.values();
	with open("hashtags_sentiment.txt", "a") as text_file:
		for value in values:
			text_file.write(str(value) + ",")
		text_file.write(str(count) + "\n\n")

	#plt.title("\"" + QUERY.upper() + "\""  + ": SENTIMENT - #TWEETS")
	#plt.scatter(data.keys(), data.values())
	#plt.show()