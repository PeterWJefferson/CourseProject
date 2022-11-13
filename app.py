from flask import Flask, request, render_template
import json

# template_folder is relative to where the main flask run .py file is (/api/app.py)
app = Flask(__name__)  # , template_folder='../templates', static_url_path="/")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/query', methods=['POST'])
def query():
    user_query = request.form['query_input']
    print(f"USER QUERY: {user_query}")
    return render_template("results.html")

#
# @app.route('/tweets', methods=['GET', 'POST'])
# def tweets():
#     api = TwitterAccess.TwitterClient()
#     if request.method == 'POST':
#         return login_user()
#     elif request.method == 'GET':
#         '''Getting the query results from Twitter and returning it to the api caller'''
#         query = json.loads(request.data)["query"]
#         tweets = api.get_tweets(query=query, count=100)
#         positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
#         return positive_tweets
#         # return ["positive_tweets"]
#
#
# @app.route('/user/<username>')
# def show_user_profile(username=None):
#     # username=None ensures the code run even when no name is provided
#     return render_template('user-profile.html', username=username)
#
#
# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     return str(post_id)
#
#
# def login_user():
#     return "You are logged in"
#
#
# def serve_login_page():
#     return "Please log in"
