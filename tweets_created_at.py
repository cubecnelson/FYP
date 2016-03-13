from pymongo import MongoClient

db = MongoClient().test
month={'Jan':'01','Feb':'02','Mar':'03','Apr':'04'}
for tweet in db.tweets.find():
	print tweet["created_at"].split(" ")[5] + month[tweet["created_at"].split(" ")[1]] + tweet["created_at"].split(" ")[2] 
