import tweepy
import time
import re
from trend import Trend
from pymongo import MongoClient
import pymongo
import json
import datetime

consumer_key = "GLc0pEAaojsnM5Kqg769QvbsD"
consumer_secret = "u2opeydedKyKc8mJcw9oQpwvgevKJdSLmSWKHh1hud0Ns9rceX"


access_token = "3241851673-19FXOYEXa0wjoRGOfMK8gxo8lcnCYpKII3C05FB"
access_token_secret = "5hS3zYdV9Z122uQBfHVFlmbq8T3NUxiOdjdyBh4m0vsCU"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

db = MongoClient().test_database

error_count = 0
dup_count = 0.0
tweet_count = 1.0


while True:
	
		pages = tweepy.Cursor(api.search, lang='en', count=200, geocode='40.7142700,-74.0059700,20km').pages()
		pages_count = 0
		print str(datetime.datetime.now()) +" Starting : TweepEr. Count (" +  str(error_count) + "), Dup. Rate (" + str(dup_count/tweet_count) + ") "
		while True:
			if pages_count >= 1000:
				break
			try:
				page = pages.next()
				pages_count = pages_count + 1
				dup_rate = dup_count/tweet_count
				print str(datetime.datetime.now()) +" Running : TweepEr. Count (" +  str(error_count) + "), Dup. Rate (" + str(dup_rate) + ") "
				dup_count = 0.0
				tweet_count = 0.0
				if dup_rate == 1.0:
					tweet_count = 1.0
					time.sleep(30)
					break
				for tweet in page:
					tweet_count = tweet_count + 1
					tweet = json.loads(json.dumps(tweet._json).replace("id", "_id"))
					try:
						db.tweets.insert_one(tweet)
					except pymongo.errors.DuplicateKeyError:
						dup_count = dup_count + 1
			except tweepy.TweepError, tweepy.error.TweepError:
				error_count = error_count + 1
				print str(datetime.datetime.now()) +" Rest : TweepEr. Count (" +  str(error_count) + "), Dup. Rate (" + str(dup_count/tweet_count) + ") "
				time.sleep(15*60)
		
	
	
		