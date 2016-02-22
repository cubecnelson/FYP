from pymongo import MongoClient
from pattern.en import parsetree
import re

db = MongoClient().test_database


tweets = db.tweets.find()
for tweet in tweets:
	myText = tweet["text"]
try:
	myText = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', myText.replace("#", "").replace("@", ""))
	tree = parsetree(myText)
	for sentence in tree:
		for chunk in sentence.chunks:
			print chunk.type, [(w.string, w.type) for w in chunk.words]

except KeyError, UnicodeEncodeError:
	print "Error"
