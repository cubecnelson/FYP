#!/usr/bin/python
import datetime
from pymongo import MongoClient
from array import array

db = MongoClient().test
hashtag_array = [] #for stroing the hashtag
hashtag_count = [] #for counting the no. of each hashtag
hashtag_len = 0 #total no. of hashtag having
filename = ""

for tweet in db.tweets.find():
	#getting date of each hashtag
	date = tweet["created_at"].split(' ')
	y = datetime.datetime.strptime(date[5]+date[1]+date[2], '%Y%b%d').date()
	#print y.strftime('%Y %b %d')
	
	#getting hashtag
	for hashtag in tweet["entities"]["hashtags"]:
		hashtext = hashtag["text"].lower()
		hashtextduplicate = False

		if hashtag_len == 0:
			hashtag_array.append(hashtext)
			hashtag_count.append(1)
			hashtag_len += 1
		else:
			for j in range(0,hashtag_len):
				if hashtag_array[j] == hashtext:
					hashtextduplicate = True
					hashtag_count[j] += 1
			if hashtextduplicate == False:
				hashtag_array.append(hashtext)
				hashtag_count.append(1)
				hashtag_len += 1
	
	#printing records for each tweet
	#time
	print y.strftime('%Y %b %d')
	#hashtags
	for j in range(0,hashtag_len):
		print (hashtag_array[j], hashtag_count[j])
		
	
	# Open a file
	#if filename != y:
	#	print ("writing")
	#	fo = open(date[5]+date[1]+date[2]+".txt", "wb")
	#	for j in range(0,hashtag_len):
	#		fo.write(hashtag_array[j])
	#		fo.write(hashtag_count[j])
	#	filename = y
		# Close opend file
	#	fo.close()