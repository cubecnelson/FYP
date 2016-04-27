import pickle
from pattern.en import parsetree
import math
import re
from pymongo import MongoClient

db = MongoClient().test_database
fileObject = open('unigram.txt', 'r')
unigramsProb = pickle.load(fileObject)
fileObject = open('bigram.txt','r')
bigramsProb = pickle.load(fileObject)

for tweet in db.tweets.find():
	prob = 1
	text = tweet["text"].encode('utf-8').lower()
	# parsetree
	text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
	# text = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", text)
	text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text.replace("#", "").replace("@", ""))
	tree = parsetree(text)
	for sentence in tree:
		for i in range(0, len(sentence.chunks)):
			try:
				if i == 0:
					prob = prob*unigramsProb[sentence.chunks[i].type.encode('utf-8')]
				if i < len(sentence.chunks) - 1:
					prob = prob*bigramsProb[(sentence.chunks[i].type.encode('utf-8'), sentence.chunks[i+1].type.encode('utf-8'))]
			except KeyError:
				continue
		try:
			print len(text.split(" ")), ":", -math.log(prob)*prob
		except ValueError:
			continue

	

