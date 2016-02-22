from pymongo import MongoClient
from pattern.en import parsetree

db = MongoClient().test_database




for tweet in db.tweets.find():
	myText = tweet["text"]
	try:
		print "Parse: ", len(parsetree(myText))

	except KeyError, UnicodeEncodeError:
		print "Error"
