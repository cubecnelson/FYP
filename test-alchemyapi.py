from pymongo import MongoClient
from alchemyapi import AlchemyAPI

db = MongoClient().test_database

alchemyapi = AlchemyAPI()


for tweet in db.tweets.find():
	myText = tweet.text
	response = alchemyapi.sentiment("text", myText.replace("#", ""))
	print ("Sentiment: ", response['docSentiment'])
