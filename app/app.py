#app folder for our instagram app, will contain app routes for traversing
#through the application

#code to start application
from json import load
from flask import Flask, render_template
app = Flask(__name__)


posts = ''
with open('static/posts.json', 'r') as read_file:
    posts = load(read_file)

@app.route("/")
@app.route("/timeline")
def home():
    return render_template('timeline.html', posts=posts)

#posting feature
@app.route("/posting" )
def post():
    return render_template('posting.html', posts=posts)
    
    


if __name__ == '__main__':
    app.run(debug=True)