#app folder for our instagram app, will contain app routes for traversing
#through the application

#code to start application
from datetime import datetime
from json import load, dump
from flask import Flask, render_template, request, url_for, redirect
from os import path
from uuid import uuid4
from forms import CommentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ErenYeager'


# load post information from json database
posts = ''
with open('app/static/posts.json', 'r') as read_file:
    posts = load(read_file)
    read_file.close()

@app.route("/", methods=['GET','POST'])
@app.route("/timeline", methods=['GET','POST'])
def timeline():
    form = CommentForm(request.form)
    if form.validate_on_submit():
        #get comment posted
        comment = form.comment.raw_data[0]
        #get post uuid
        parentID = form.parentID.raw_data[0]
        #get post author (will later be changed to current_user)
        author = form.author.raw_data[0]
        #loop through posts until we find the post with a matching uuid
        for post in posts:
            if post['uuid'] == parentID:
                comment_data = {'author': author, 'comment': comment}
                #update list of comments for that post
                post['comments'].append(comment_data)
                break
        with open('app/static/posts.json', 'w') as all_posts:
            dump(posts, all_posts, indent=4, sort_keys=True)
        return redirect(url_for('timeline'))

    return render_template('timeline.html', posts=posts, form = form)

#posting feature
@app.route("/posting")
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
    new_post['uuid'] = str(uuid4())
    new_post['author']      = poster_name
    new_post['description'] = description
    new_post['image']       = img_file.filename
    new_post['date_posted'] = date
    new_post['comments'] = list()

    with open('app/static/posts.json', 'w') as all_posts:
        posts.insert(0, new_post)
        dump(posts, all_posts, indent=4, sort_keys=True)
        all_posts.close()

    return redirect(url_for('timeline'))
   


    



    
    

    


    


if __name__ == '__main__':
    app.run(debug=True)