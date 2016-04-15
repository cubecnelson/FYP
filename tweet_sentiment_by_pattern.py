from pymongo import MongoClient
import pymongo
from pattern.en import sentiment
import numpy as np
import matplotlib.pyplot as plt
import math
import re

db = MongoClient().test_database

for trend in db.trends.find():
	try:
		count = 0.0
		
		

		print trend['_id'].encode('utf-8')
		QUERY = trend['_id']

		QUERY = QUERY.lower()

		record = []

		zeros = np.linspace(0,1,10)

		data = {}

		for zero in zeros:
			try:
				zero = math.ceil(zero*10)/10
				data[zero] = 0.0
				data[0.1] = 0.0
			except KeyError:
				data[zero] = 0.0
				break



		#plt.show()
		for tweet in db.tweets.find({"entities.hashtags.text": re.compile(QUERY, re.IGNORECASE)}):
			myText = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet["text"].replace("#", "").replace("@", ""))
			response = math.ceil(sentiment(myText.replace("#", ""))[0]*10)/10
			response = abs(response)
			if response != 0.0:
				count = count + 1.0
				try:
					data[response] = data[response] + 1.0
				except KeyError:
					data[response] = 1.0
					
		print data
			
		if count != 0:
			for key in data.keys():
				data[key] = data[key]/count

		print str(len(data.values()))

		db.train_data.insert({
			"_id": trend["_id"],
			"count":count,
			"values":data.values()
		});

		#values = data.values();
		#with open("hashtags_sentiment.txt", "a") as text_file:
		#	for value in values:
		#		text_file.write(str(value) + ",")
		#	text_file.write(str(count) + "\n\n")
	except pymongo.errors.CursorNotFound:
		continue
