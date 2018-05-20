from twython import TwythonStreamer
import json
import string

def make_printable(s):
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, s))

def process_tweet(tweet):
    d = {tweet['user']['id']:{
    # 'name': tweet['user']['name'],
    # 'screen_name': tweet['user']['name'],
    # 'created_at': tweet['created_at'],
    # 'text': tweet['text']
    'name': make_printable(tweet['user']['name']),
    'screen_name': make_printable(tweet['user']['name']),
    'created_at': make_printable(tweet['created_at']),
    'text': make_printable(tweet['text'])
    }}
    return d

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if data['lang'] == 'en':
            tweet_data = process_tweet(data)
            self.save_to_json(tweet_data)

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

    def save_to_json(self, tweet):
        with open('search_results.json') as f:
            data = json.load(f)

        data.update(tweet)

        with open('search_results.json', mode = 'a') as f:
            json.dump(data, f)


with open('search_results.json', mode = 'w') as f:
    primer = {}
    json.dump(primer, f)

with open('twitter_credentials.json') as f:
    credentials = json.load(f)

APP_KEY = credentials['CONSUMER_KEY']
APP_SECRET = credentials['CONSUMER_SECRET']
ACCESS_TOKEN = credentials['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = credentials['ACCESS_TOKEN_SECRET']

stream = MyStreamer(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
stream.statuses.filter(track = 'death,rainbow,kill')
