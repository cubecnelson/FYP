import tweepy
import time
import re
from trend import Trend
import json

consumer_key = "GLc0pEAaojsnM5Kqg769QvbsD"
consumer_secret = "u2opeydedKyKc8mJcw9oQpwvgevKJdSLmSWKHh1hud0Ns9rceX"

access_token = "3241851673-19FXOYEXa0wjoRGOfMK8gxo8lcnCYpKII3C05FB"
access_token_secret = "5hS3zYdV9Z122uQBfHVFlmbq8T3NUxiOdjdyBh4m0vsCU"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

f = open("tweets.txt", "a")

id_list = []
while True:
	

	page = 1

	tweets = api.search(lang='en', rpp=100, page=page,  geocode='40.7142700,-74.0059700,15.8476023485km')
	while tweets:
		for tweet in tweets:
			
			if tweet.id not in id_list:
				f = open("tweets.txt", "a")
				print ('Tweet ', tweet.id , ': ', tweet.text.encode("utf-8"))
				id_list.append(tweet.id)
				f.write(str(tweet.id) + ": " + str(tweet.text.encode("utf-8")) + '\n')
				f.close()
		page = page + 1
		tweets = api.search(page=page, lang='en', count=200, geocode='40.7142700,-74.0059700,15.8476023485km')

	time.sleep(5)
