#app folder for our instagram app, will contain app routes for traversing
#through the application

#code to start application
from datetime import datetime
from json import load, dump
from flask import Flask, render_template, request, url_for, redirect
from os import path

app = Flask(__name__)


posts = ''
with open('static/posts.json', 'r') as read_file:
    posts = load(read_file)

@app.route("/")
@app.route("/timeline")
def timeline():
    return render_template('timeline.html', posts=posts)

#posting feature
@app.route("/posting" )
def post():
    return render_template('posting.html', posts=posts)


@app.route("/posting", methods=['POST'])
def image_post():

    #Placeholder name. Will be replaced once user database is implemented.
    poster_name = "Default"

    date = datetime.today().strftime("%d/%m/%Y")
    
    img_file = request.files['file']
    description = request.form['description']

    if img_file.filename == "":
        print("No file selected")
        return redirect(url_for('post'))

    file_path = path.join(app.root_path, 'static/images', img_file.filename)
    img_file.save(file_path)

    new_post = {}
    new_post['author']      = poster_name
    new_post['description'] = description
    new_post['image']       = img_file.filename
    new_post['date_posted'] = date

    with open('app/static/posts.json', 'w') as all_posts:
        posts.insert(0, new_post)
        dump(posts, all_posts)

    return redirect(url_for('timeline'))
   


    



    
    

    


    


if __name__ == '__main__':
    app.run(debug=True)