import math
import numpy
import nltk
import re
import time
from pymongo import MongoClient
from pattern.en import ngrams
from nltk.util import bigrams
from decimal import *
from itertools import chain
from itertools import tee, izip
from nltk.probability import ConditionalFreqDist
import unicodedata
from pattern.en import parsetree

db = MongoClient().test_database

def tokenize(line):
	list = line.split()
	tokens = []
	for item in list:
		while re.match('\W',item):
			# non-alphnumeric item at beginning of item
			tokens.append(item[0])
			item = item[1:]
			# to maintain order, we use temp
			temp = []
			while re.search('\W$',item):
				# non-alphnumeric item at end of item
				temp.append(item[-1])
				item = item[:-1]
				# Contraction handling
				if item == "can't":
					tokens.append("can")
					tokens.append("n't")
					# other n't words:
				elif re.search("n't",item):
					tokens.append(item[:-3])
					tokens.append(item[-3:])
					# other words with apostrophes ('s, 'll, etc.)
				# elif re.search("'",item):
				# 	wordlist = item.split("'")
				# 	tokens.append(wordlist[0])
				# 	tokens.append("'"+wordlist[1])
					# no apostrophe, i.e., normal word:
				else:
					tokens.append(item)
					tokens.extend(temp[::-1])
	return tokens

def dictionarycheck(word, dictionary):
	word = word.lower()
	if word in dictionary:
		print type(dictionary[word]), dictionary[word]
		return dictionary[word]
	else:
		return False

def ngrams(sentence, n):
  return zip(*[sentence.split()[i:] for i in range(n)])

def overallProb(tokens, unigramsProb, bigramsProb):
	prob = 1.0
	prev_token = ""
	for tidx, token in enumerate(tokens):
		# add-one smoothing on unigram
		if token not in unigramsProb:
			unigrams[token] = 1
			print "token count: ", sum(unigrams.values())
			unigramsProb[token] = 1.0/sum(unigrams.values())
			print "new unigramProb: ", unigramsProb[token]
		if tidx == 0:
			prob *= unigramsProb[token]
			prev_token = token
		else:
			prob *= bigramsProb[(prev_token, token)]
			prev_token = token
	return prob

def convertUnicodeToString(unicodeText):
	unicodedata.normalize('NFKD', unicodeText).encode('ascii','ignore')
	return unicodeText

unigrams = {}
count = 0
tokens = []
train_tokens = []
test_tokens = []
unigramsProb = {}
bigramsProb = {}
tweetProb = []
cfd = ConditionalFreqDist()
# o = Observable()

tweets = db.tweets.find()	

for idx, tweet in enumerate(tweets[0:100]):
	text = tweet["text"].encode('utf-8').lower()
	# parsetree
	text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
	# text = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", text)
	text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text.replace("#", "").replace("@", ""))
	tree = parsetree(text)
	for sentence in tree:
		for chunk in sentence.chunks:
			tokens.append(chunk.type.encode('utf-8'))
	# tokenize(text)
	# tokens = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
	# tokens = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", tokens)
	if idx <= 90:
		train_tokens.append(tokens)

		# Unigrams
		for words in train_tokens[0:]:
			for word in words:
				if word in unigrams:
					unigrams[word] += 1 
				else:
					unigrams[word] = 1
		# unigrams prob
		if len(unigrams) != 0:
			for unigram in unigrams:
				unigramsProb[unigram] = float(unigrams[unigram])/len(unigrams)

		# Bigrams
		for word in train_tokens[0:]:
			x = ngrams(" ".join(word), 2)
			for bg in x:
				cfd[bg[0]][bg[1]] += 1
		cfd = ConditionalFreqDist((bg[0],bg[1]) for bg in list(chain(*[bigrams(i) for i in train_tokens])))
		if (idx >= 90):
			for bgidx, bg in enumerate(list(chain(*[bigrams(i) for i in train_tokens]))):
			    prob = cfd[bg[0]].freq(bg[1])
			    prob = 0.0001 if not prob else prob
			    bigramsProb[bg] = prob
	if (idx >= 90):
		test_tokens.append(tokens)
		if idx >= 190:
			for bgidx, bg in enumerate(list(chain(*[bigrams(i) for i in test_tokens]))):
			    prob = cfd[bg[0]].freq(bg[1])
			    prob = 0.0001 if not prob else prob
			    bigramsProb[bg] = prob
			tweetProb.append(overallProb(tokens, unigramsProb, bigramsProb))

for elem in train_tokens:
	print elem
print "unigrams: ", unigrams
print "unigramsProb: ", unigramsProb
print "bigramsProb: ", bigramsProb
print "tweets Prob: ", tweetProb
print "tweets length: ", len(tweetProb)
	# print "tweet ", idx, " : ", unigramsProb
	# # Overall Prob of Tweets
	# prob = 1.0
	# prev_token = ""
	# for tidx, token in enumerate(tokens):
	# 	print tidx, token, bigramsProb
	# 	if tidx == 0:
	# 		prob *= unigramsProb[token]
	# 		prev_token = token
	# 	else:
	# 		prob *= bigramsProb[prev_token][token]
	# 	print prob



		# for word in words:
		# 	bigram = prev_word + " " + word
		# 	if bigram in bigrams:
		# 		bigrams[bigram] += 1
		# 	else:
		# 		bigrams[bigram] = 1
		# 	prev_word = word
		# for bigram in bigrams:
		# 	temp = bigram.split()
		# 	cfd[temp[0]].inc(temp[1])
		# 	print cfd[temp[0]].freq(temp[1])
		# 	bigramsProb[bigram] = math.log(float(float(bigrams[bigram])/len(bigrams))/unigramsProb[temp[0]], 2)
		# print bigramsProb
		# # 	biCount = len(bigrams)



# print "--------Bigrams---------"
# print bigrams, biCount

# # # if len(bigrams) != 0:
	# for bigram in bigrams:
	# 	bigramsProb[bigram] = float(bigrams[bigram])/len(bigrams)
	# print "Bigrams Prob: ", bigramsProb

# # check whether the test input exist in unigrams model
# test_word = raw_input("Input a word to test: ")
# word_prob = dictionarycheck(test_word, unigramsProb)
# print "word Prob in Unigrams: ", word_prob





