from trend import Trend
from pymongo import MongoClient
import pymongo
import json
from stemming.porter2 import stem

db = MongoClient().test_database

trends = []

for tweet in db.tweets.find():
	for hashtag in tweet["entities"]["hashtags"]:
		try:
			print hashtag['text'].encode("utf-8").lower()
			result = db.trends.insert_one({
				"_id" : hashtag['text'].encode("utf-8").lower()
			})
		except pymongo.errors.DuplicateKeyError:
			print "ERROR"