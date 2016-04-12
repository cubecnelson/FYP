from pymongo import MongoClient
from array import array

db = MongoClient().test

month = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
db.searchHashtagCounts.drop()
# db.searchHashtagCounts

# targetDate = '_20160213'
# db[targetDate]	# create collection with target date as the name

for tweet in db.tweets.find():
	tweetDate = tweet["created_at"].split(" ")[5] + month[tweet["created_at"].split(" ")[1]] + tweet["created_at"].split(" ")[2] 
	
	for hashtag in tweet["entities"]["hashtags"]:
		hashtext = hashtag["text"].lower()
		if db.collectionExists(hashtext) == False:
			db[hashtext] # create collection with hashtag as the name
			
		result = db[hashtext].find_one({"Date": tweetDate})
		if result == None:
			db[hashtext].insert_one(
				{
					"_id": tweetDate, 
					"Date": tweetDate, 
					"count": 1
				}	
			)
		else:
			db[hashtext].update_one(
				{"_id": tweetDate},
				{
					"$inc": {
						"count": 1}}
			)
#for resultCounts in db.christmas.find():
#	print resultCounts