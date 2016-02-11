import tweepy
from pattern.en import parse
from pattern.web import Twitter,plaintext
import time

consumer_key = "GLc0pEAaojsnM5Kqg769QvbsD"
consumer_secret = "u2opeydedKyKc8mJcw9oQpwvgevKJdSLmSWKHh1hud0Ns9rceX"

access_token = "3241851673-19FXOYEXa0wjoRGOfMK8gxo8lcnCYpKII3C05FB"
access_token_secret = "5hS3zYdV9Z122uQBfHVFlmbq8T3NUxiOdjdyBh4m0vsCU"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

trends = api.trends_place(id='23424977')

trends = trends[0]

trends = trends['trends']

for trend in trends:
	print 'Trends: ' + trend['name'] + '\n'
	
	twitter = Twitter(language="en")
	n = 0
	for tweet in twitter.search(trend["name"], cached=False):
		print str(n) + ": " + tweet.text.encode('utf-8') +  "\n"
		n = n + 1