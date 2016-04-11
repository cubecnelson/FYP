from pymongo import MongoClient

db = MongoClient().test_database
db.hi
hashtag = "hi"

print db.hi.update_one({"_id":"a"}, {'$inc': {"count": -1}})

for hi in db.hi.find():
	print hi