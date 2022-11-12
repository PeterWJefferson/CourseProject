from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/greet')
def say_hello():
  return 'Hello from Server'

@app.route('/user/<username>')
def show_user_profile(username=None):
    #username=None ensures the code run even when no name is provided
    return render_template('user-profile.html', username=username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return str(post_id)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #check user details from db
        return login_user()
    elif request.method == 'GET':
        #serve login page
        return serve_login_page()

def login_user():
    return "You are logged in"

def serve_login_page():
    return "Please log in"

