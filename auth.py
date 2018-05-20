from twython import TwythonStreamer
import json
import string
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def make_printable(s):
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, s))
    # return clean_text(''.join(filter(lambda x: x in printable, s)))

# def clean_text(s):
#     sn = s.split(' ')
#     return ''.join([x for x in sn if '@' not in x])

def calc_sentiment(text):
    blob = TextBlob(text, analyzer = NaiveBayesAnalyzer())
    return (blob.sentiment.p_pos, blob.sentiment.p_neg)

def process_tweet(tweet):
    p_pos, p_neg = calc_sentiment(make_printable(tweet['text']))
    id = tweet['user']['id']

    with open('search_results.json', 'r') as f:
        data = json.load(f)

        if id not in data.keys():
            d = {id: {
            'name': make_printable(tweet['user']['name']),
            'screen_name': make_printable(tweet['user']['name']),
            'text': make_printable(tweet['text']),
            'p_pos': p_pos,
            'n_pos': p_neg,
            'dep_score': 0
            }}
        else:
            d = {id: {
            'name': make_printable(tweet['user']['name']),
            'screen_name': make_printable(tweet['user']['name']),
            'text': make_printable(tweet['text']),
            'text': make_printable(tweet['text']),
            'p_pos': data[id]['p_pos'] + p_pos,
            'n_pos': data[id]['n_pos'] + n_pos,
            'dep_score': data[id]['dep_score']
            }}

    return d

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if data['lang'] == 'en':
            tweet_data = process_tweet(data)
            self.save_to_json(tweet_data)
            # print tweet_data

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

    def stop_loop(self):
        self.disconnect()
        print '\nStream stopped.'

    def save_to_json(self, tweet):
        with open('search_results.json') as f:
            data = json.load(f)

        data.update(tweet)

        with open('search_results.json', 'w') as f:
            json.dump(data, f)

def run_stream(keywords):
        stream.statuses.filter(track = keywords)

with open('twitter_credentials.json') as f:
    credentials = json.load(f)

APP_KEY = credentials['CONSUMER_KEY']
APP_SECRET = credentials['CONSUMER_SECRET']
ACCESS_TOKEN = credentials['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = credentials['ACCESS_TOKEN_SECRET']

stream = MyStreamer(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
