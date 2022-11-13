import tweepy
import re
from flask import Flask
from tweepy import OAuthHandler
from textblob import TextBlob

app = Flask(__name__)


class TwitterClient(object):

    def __init__(self):
        F = open('API_Keys.txt', 'r').readlines()

        consumer_key = F[0].split(":")[1].strip()
        consumer_secret = F[1].split(":")[1].strip()
        access_token = F[2].split(":")[1].strip()
        access_token_secret = F[3].split(":")[1].strip()
        bearer_token = r"AAAAAAAAAAAAAAAAAAAAAOXwjAEAAAAAzSEYMbVvuYyDEBs%2FMzrCfArRD1o%3D0GLEDRL8dClUcsUyXmkrIxLS9WsTillEnyAOFkHDymoNMqbGPf"
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
            self.client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        """
      Utility function to clean tweet text by removing links, special characters
      using simple regex statements.
      """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        """
      Utility function to classify sentiment of passed tweet
      using textblob's sentiment method
        """
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        """
      Main function to fetch tweets and parse them.
      """
        tweets = []

        try:
            # With this, I get the error: AttributeError: 'API' object has no attribute 'search'. This could be a
            # versioning issue fetched_tweets = self.api.search(q = query, count = count)
            fetched_tweets = self.api.search_tweets(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        # The commented code gave me the error: AttributeError: module 'tweepy' has no attribute 'TweepError'. This
        # could be a versioning issue except tweepy.TweepError as e:
        except tweepy.errors.TweepyException as e:
            print("Error : " + str(e))


def search():
    query = input("What would you like to search on Twitter?\n")
    return query


def main(_query):
    api = TwitterClient()
    query_ = _query
    #   When count = 200, I get the error: Max retries exceeded with url: /1.1/search/tweets.json
    #   tweets = api.get_tweets(query = query_, count = 200)
    tweets = api.get_tweets(query=query_, count=50)
    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100 * len(positive_tweets) / len(tweets)))

    negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100 * len(negative_tweets) / len(tweets)))

    print("Neutral tweets percentage: {} % \
      ".format(100 * (len(tweets) - (len(negative_tweets) + len(positive_tweets))) / len(tweets)))

    print("\n\nPositive tweets:")
    for tweet in positive_tweets[:10]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in negative_tweets[:10]:
        print(tweet['text'])


if __name__ == "__main__":
    main()
