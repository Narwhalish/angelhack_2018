import tweepy
import json
from pprint import pprint #pretty print to ease debugging

# Consumer keys and access tokens, used for OAuth
with open('twitter_credentials.json') as f:
    credentials = json.load(f)

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(credentials['CONSUMER']['KEY'], credentials['CONSUMER']['SECRET'])
auth.set_access_token(credentials['ACCESS']['TOKEN'], credentials['ACCESS']['SECRET'])

# Creation of the actual interface, using authentication
api = tweepy.API(auth)
