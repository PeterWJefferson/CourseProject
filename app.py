from flask import Flask, request, render_template, redirect, url_for
from gensim.parsing.preprocessing import remove_stopwords, strip_punctuation, strip_short, strip_non_alphanum
import json
import TwitterAccess
from Plsa import *
from sources import *

# template_folder is relative to where the main flask run .py file is (/api/app.py)
app = Flask(__name__)  # , template_folder='../templates', static_url_path="/")


@app.route('/')
def index():
    recommended_topics = []
    # Call our Topic Modeling function using recent search topics as input to display recommended searches
    recommended_topics = get_topics()

    # If there is nothing in the recent search file, just return generic political topics for the first search
    # if len(recommended_topics) < 1:
    #     recommended_topics = ["biden", "trump", "healthcare", "Ukraine war"]

    return render_template("index.html", recommended_search_topics=recommended_topics)


@app.route('/delete_search_topics', methods=['POST'])
def delete_search_topics():

    # TODO: Call function that deletes the stored search topic history.

    return render_template("index.html")


@app.route('/query', methods=['POST'])
def query():
    user_query = request.form['query_input']
    print(f"USER QUERY: {user_query}")

    # Hold the selected news sources to explicitly search if user selected any.
    list_of_news_accounts_to_search = []
    # Hold the number of sentiments (positive, neutral, negative) for each news source
    news_source_sentiments = {}
    # Go through each HTML checkbox and append the ones that have been selected, if any, to the
    #  list_of_news_accounts_to_search list.
    for news_source_name in news_source_names:
        if request.form.get(news_source_name) is not None:
            list_of_news_accounts_to_search.append(news_source_name)

    if list_of_news_accounts_to_search:
        print(f"Only searching the following News source Twitter account(s): {list_of_news_accounts_to_search}")
        tweets_to_display = news_tweets(user_query=user_query, news_sources=list_of_news_accounts_to_search)
        # Calculate the sentiments total by news source to display them.
        for news_account in list_of_news_accounts_to_search:
            news_source_sentiments[news_account] = [{'positive': 0,
                                                     'neutral': 0,
                                                     'negative': 0}, 0]
        for tweet in tweets_to_display:
            news_account = tweet['source']
            tweet_sentiment = tweet['sentiment']
            news_source_sentiments[news_account][0][tweet_sentiment] += 1
            news_source_sentiments[news_account][1] += 1

        # Calculate the percentage of sentiments for each news account
        for account in news_source_sentiments.keys():
            positive = news_source_sentiments[account][0]['positive']
            neutral = news_source_sentiments[account][0]['neutral']
            negative = news_source_sentiments[account][0]['negative']

            total = positive + neutral + negative

            if total > 0:
                positive_percent = positive / total
                neutral_percent = neutral / total
                negative_percent = negative / total

                news_source_sentiments[account][0]['positive'] = round(positive_percent * 100, 2)
                news_source_sentiments[account][0]['neutral'] = round(neutral_percent * 100, 2)
                news_source_sentiments[account][0]['negative'] = round(negative_percent * 100, 2)

        print(news_source_sentiments)

    else:
        print(f"No explicit news source(s) selected, so searching all of twitter...")
        tweets_to_display = tweets(user_query=user_query)

    return render_template("results.html", tweet_list=tweets_to_display, query=user_query,
                           news_sentiments=news_source_sentiments)


@app.route('/upvote')
def upvote_post():
    # TODO: Enter logic to take the tweet and put it in user DB
    return "nothing"


@app.route('/tweets', methods=['GET', 'POST'])
def tweets(user_query):
    api = TwitterAccess.TwitterClient()
    if request.method == 'POST':
        '''Getting the query results from Twitter and returning it to the api caller'''
        tweets = api.get_tweets(query=user_query, count=50)
    tweet_corpus = open('data/tweet_corpus.txt', 'a', encoding='utf-8')
    if tweets:
        for tweet in tweets:
            clean_tweet = strip_short(strip_punctuation(remove_stopwords(strip_non_alphanum(tweet['text']))), minsize=5).lower()
            searches = api.get_recent_searches()
            print("This is the cleaned tweet prior to checking for searched terms: ", clean_tweet)
            if len(searches) > 1:
                for search in searches:
                    for word in search.split():
                        if word.lower() in clean_tweet:
                            clean_tweet = clean_tweet.replace(word, "").replace("  ", " ")
                        if "https" in clean_tweet:
                            clean_tweet = clean_tweet.replace("https", "").replace("  ", " ")
                        if "http" in clean_tweet:
                            clean_tweet = clean_tweet.replace("http", "").replace("  ", " ")
            #cleaning again because sometimes after removing unwanted 'words' such as recently searched words, it can leave a lonesome trailing 's' behind
            clean_tweet = strip_short(strip_punctuation(remove_stopwords(strip_non_alphanum(clean_tweet))), minsize=5).lower()
            print("This is the cleaned tweet after checking for searched terms: ", clean_tweet)
            tweet_corpus.write("{}\n".format(clean_tweet.replace("\n", " ")))
        return tweets


@app.route('/tweets/news', methods=['GET', 'POST'])
def news_tweets(user_query=None, news_sources=[]):
    if user_query:
        query = user_query
    else:
        query = request.form['query_input']

    api = TwitterAccess.TwitterClient()
    tweets = []
    if request.method == 'POST':
        '''Getting the query results from Twitter and returning it to the api caller'''
        tweets = api.query_twitter_users(query=query, count=50, user_list=news_sources)
    tweet_corpus = open('data/tweet_corpus.txt', 'a')
    if tweets:
        for tweet in tweets:
            clean_tweet = strip_short(strip_punctuation(remove_stopwords(strip_non_alphanum(tweet['text']))), minsize=5)
            tweet_corpus.write("{}\n".format(clean_tweet.replace("\n", " ").lower()))
    return tweets


@app.route('/tweets/init', methods=['GET', 'POST'])
def tweets_init():
    api = TwitterAccess.TwitterClient()
    tweets = []
    '''Getting the recent tweets from out news sources'''
    tweets = api.query_twitter_users(query=None, count=50, user_list=news_sources)
    return tweets

@app.route('/tweets/topics', methods=['GET', 'POST'])
def get_toptics():
    trends = []
    '''Getting trends based on recent tweets and recent queries'''
    trends = get_topics()
    return {"trends": trends}


@app.route('/user/<username>')
def show_user_profile(username=None):
    # username=None ensures the code run even when no name is provided
    return render_template('user-profile.html', username=username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return str(post_id)


def clean_tweets(tweet_list):
    """
    Takes in a list of returned tweets from the Twitter api, cleans, adn returns them.
    :param tweet_list: list of dictionary tweets
    :return: list of clean tweets
    """


def login_user():
    return "You are logged in"


def serve_login_page():
    return "Please log in"
