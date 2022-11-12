import os
import tweepy

client = tweepy.Client(bearer_token=os.getenv('bearer_token'))

#search by word match
# response = client.search_recent_tweets("biden")

#search by user id received from https://api.twitter.com/2/users/by/username/:username (e.g., nytimes = 807095, FoxNews = 1367531)
nytimes_user_id = 2244994945
fox_news_user_id = 1367531
nytimes_response = client.get_users_tweets(nytimes_user_id)
fox_news_response = client.get_users_tweets(fox_news_user_id)


# The method returns a Response object, a named tuple with data, includes,
# errors, and meta fields
# print(response.meta)

# In this case, the data field of the Response returned is a list of Tweet
# objects
nytimes_tweets = nytimes_response.data
fox_news_tweets = fox_news_response.data

tweets = nytimes_tweets + fox_news_tweets

# Each Tweet object has default ID and text fields
for tweet in tweets:
    print(tweet.id)
    print(tweet.text)

# By default, this endpoint/method returns 10 results
# You can retrieve up to 100 Tweets by specifying max_results
# response = client.search_recent_tweets("Tweepy", max_results=100)