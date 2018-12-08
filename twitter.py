import tweepy
import pandas as pd
import numpy as np
import csv

from IPython.display import display
import matplotlib.pyplot as plt

from creds import *

def setup():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

extractor = setup()

csvFile = open('tweets.csv', 'a')
csvWriter = csv.writer(csvFile)
tweets = 0

for tweet in tweepy.Cursor(extractor.user_timeline, screen_name='@realDonaldTrump',
                            tweet_mode="extended").items():
    tweets = tweets + 1
    csvWriter.writerow([tweet.created_at, tweet.full_text.encode('utf-8')])

print(tweets)
csvFile.close()
