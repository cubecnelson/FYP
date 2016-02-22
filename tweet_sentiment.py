from pymongo import MongoClient
from alchemyapi import AlchemyAPI

db = MongoClient().test_database

alchemyapi = AlchemyAPI()


for tweet in db.tweets.find():
	myText = tweet["text"]
	response = alchemyapi.sentiment("text", myText.replace("#", ""))
	#try:
	print "Sentiment: " , response
	#except KeyError, UnicodeEncodeError:
	#	print "Error"
