from pymongo import MongoClient
from array import array

db = MongoClient().test
month={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
# hashtagArray = [][0] #store [hashtagName][count]
hashtagArray=[[0 for j in range(2)]] #store [[hashtagName,count],[hashtagName,count]...]
hashtag_len = 0 #total no. of hashtag having

for tweet in db.tweets.find():
	tweetDate = tweet["created_at"].split(" ")[5] + month[tweet["created_at"].split(" ")[1]] + tweet["created_at"].split(" ")[2] 
	
	# '20160213' is a substring of tweetDate
	if '20160213' in tweetDate:
		for hashtag in tweet["entities"]["hashtags"]:
			hashtext = hashtag["text"].lower()
			# when hashtagArray is empty
			if hashtag_len == 0:
				hashtagArray.append([hashtext,1])
				hashtag_len += 1
			else:
				for i in range(0,hashtag_len):
					if hashtext == hashtagArray[i][0]:
						hashtagArray[i][1] += 1
					else:
						hashtagArray.append([hashtext,1])
						hashtag_len += 1

for x in range(0,hashtag_len):
	print hashtagArray[x]
