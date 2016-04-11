import tweepy
import time
import re
from trend import Trend
from pymongo import MongoClient
import pymongo
import json
import datetime

consumer_key = ["GLc0pEAaojsnM5Kqg769QvbsD","6SC10uTkT9qbvjnZ18i97UgRX", "yZHC6IWkYs0hvaqQEY67FXjTt"]
consumer_secret = ["u2opeydedKyKc8mJcw9oQpwvgevKJdSLmSWKHh1hud0Ns9rceX", "spHJG5JHlNq8DCxKgpfWhLlk8IhGyqBrLDQZnI0Nw6C3X2Rcbc", "eKJP8NfZa4IVvwZfl0DRdDFGm5jc0i8rSt5Q5xX385VtRHUNWy"]


access_token = ["3241851673-19FXOYEXa0wjoRGOfMK8gxo8lcnCYpKII3C05FB", "701612704927068161-d2raL7vmHHE0wJLDJaPhKOyw8ZMZ0rg", "3305232200-JhHyQgGy7blHYaywWdeATATymY4rkHg3rkA5CV4"]
access_token_secret = ["5hS3zYdV9Z122uQBfHVFlmbq8T3NUxiOdjdyBh4m0vsCU", "dAdkAiBTPxtgrmPw8w7vh7zukBGRKfAX3XERhEOjG04VV", "6a7AUktb9BHax0FMxAK37zWwOsdX48nl8nH4h45wQkw9t"]


auth = tweepy.OAuthHandler(consumer_key[0], consumer_secret[0])
auth.set_access_token(access_token[0], access_token_secret[0])

api = tweepy.API(auth)

db = MongoClient().test_database

error_count = 0
dup_count = 0.0
tweet_count = 1.0
auth_int = 0

while True:
		
		pages = tweepy.Cursor(api.search, lang='en', count=200, geocode='40.7142700,-74.0059700,20km').pages()
		pages_count = 0
		print str(datetime.datetime.now()) +" Starting : TweepEr. Count (" +  str(error_count) + "), Dup. Rate (" + str(dup_count/tweet_count) + ") "
		while True:
			#if pages_count >= 1000:
			#	break
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
				if auth_int == len(consumer_key)-1:
					auth_int = 0
					auth = tweepy.OAuthHandler(consumer_key[auth_int], consumer_secret[auth_int])
					auth.set_access_token(access_token[auth_int], access_token_secret[auth_int])
				else:
					auth_int = auth_int + 1
					auth = tweepy.OAuthHandler(consumer_key[auth_int], consumer_secret[auth_int])
					auth.set_access_token(access_token[auth_int], access_token_secret[auth_int])
					api = tweepy.API(auth)
				break

		
	
	
		