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
from array import array
from pattern.en import sentiment
import numpy as np

db = MongoClient().test_database
month = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}



QUERY = 'type1diabetes'



for tweet in db.tweets.find({"entities.hashtags.text": re.compile(QUERY, re.IGNORECASE)}).sort([("_id", pymongo.DESCENDING)]):
	tweetDate = tweet["created_at"].split(" ")[5] + month[tweet["created_at"].split(" ")[1]] + tweet["created_at"].split(" ")[2] 
	myText = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet["text"].replace("#", "").replace("@", ""))
	response = math.ceil(sentiment(myText.replace("#", ""))[0]*10)/10
	response = int(abs(response*10))

	nameExist = False
	for name in db.collection_names():
		if name == QUERY:
			nameExist == True
	if nameExist == False:
		db[QUERY] # create collection with hashtag as the name
	
	result = db[QUERY].find_one({"Date": tweetDate})
	if result == None:
		data = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0}
		
		data[str(int(response))] = data[str(int(response))] + 1.0
			
		db[QUERY].insert_one(
			{
				"_id": tweetDate, 
				"Date": tweetDate, 
				"count": 1, 
				"sentiment": data
			}	
		)
	else:
		data = result["sentiment"]
		
		data[str(response)] = data[str(response)] + 1.0
				
		db[QUERY].update_one(
			{"_id": tweetDate},
			{
				"$inc": {
					"count": 1},
				"$set": {
					"sentiment": data}
			}
		)
