#app folder for our instagram app, will contain app routes for traversing
#through the application

#code to start application
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/timeline")
def home():
    return render_template('timeline.html')


if __name__ == __'main__':
    app.run(debug=True)