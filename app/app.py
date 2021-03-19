#app folder for our instagram app, will contain app routes for traversing
#through the application

#code to start application
from datetime import datetime
from json import load, dump
from flask import Flask, render_template, request, url_for, redirect, flash, session
from os import path
from uuid import uuid4
from forms import CommentForm, Register, Login, Follow, Unfollow
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length
from jinja2 import Environment

from wtforms_components import validators
jinja_env = Environment()


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config['SECRET_KEY'] = 'ErenYeager'

# load post information from json database
posts = ''
with open('app/static/posts.json', 'r') as read_file:
    posts = load(read_file)
    read_file.close()
accounts = ''
with open('app/static/accounts.json', 'r') as read_accounts:
    accounts = load(read_accounts)

def follow(followee, follower):
    for account in accounts:
        if account['username'] == followee:
            account['following'].append(follower)
            with open('app/static/accounts.json', 'w') as all_accounts:
                dump(accounts, all_accounts, indent=4, sort_keys=True)

def unfollow(followee, follower):
    for account in accounts:
        if account['username'] == followee:
            account['following'].remove(follower)
            with open('app/static/accounts.json', 'w') as all_accounts:
                dump(accounts, all_accounts, indent=4, sort_keys=True)

@app.route("/", methods=['GET','POST'])
@app.route("/timeline", methods=['GET','POST'])
def timeline():
    form = CommentForm(request.form)
    follow_form = Follow(request.form)
    unfollow_form = Unfollow(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            #get comment posted
            comment = form.comment.raw_data[0]
            #get post uuid
            parentID = form.parentID.raw_data[0]
            #get post author (will later be changed to current_user)
            author = form.author.raw_data[0]
            #loop through posts until we find the post with a matching uuid
            if 'comment' in request.form:
                for post in posts:
                    if post['uuid'] == parentID:
                        comment_data = {'author': author, 'comment': comment}
                        #update list of comments for that post
                        post['comments'].append(comment_data)
                        break
                with open('app/static/posts.json', 'w') as all_posts:
                    dump(posts, all_posts, indent=4, sort_keys=True)
            return redirect(url_for('timeline'))
        if 'follow_user' in request.form:
            follow(session.get('username'), request.form.get('follow_user'))
        if 'unfollow_user' in request.form:
            unfollow(session.get('username'), request.form.get('unfollow_user'))
    return render_template('timeline.html', posts=posts, form = form, username=session.get('username'), accounts=accounts, follow_form=follow_form, unfollow_form=unfollow_form)

#posting feature
@app.route("/posting")
def post():
    return render_template('posting.html', posts=posts, username=session.get('username'))


@app.route("/posting", methods=['POST'])

def image_post():
    
    poster_name = session.get('username')

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
   



def valid(username, password):
    with open('app/static/accounts.json', 'r') as accounts_file:
                accounts = load(accounts_file)
    for account in accounts:
        if username == account['username'] and password == account['password']:    
            return True
    return False


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login()
    if form.validate_on_submit():
        if valid(form.username.data, form.password.data):
            username = form.username.data
            session['username'] = form.username.data
            flash(username + " is logged in",category='username is logged in')
            return redirect(url_for('timeline'))
        else:
            flash("Your USERNAME/PASSWORD might be incorrect!" , category='loginerror')
    return render_template("login.html", form=form, posts=posts)

@app.route("/register",methods=['POST','GET'])
def signup():
    form = Register()
    if request.method == 'POST':
        if form.validate_on_submit():
            with open('app/static/accounts.json', 'r') as accounts_file:
                accounts = load(accounts_file)

            for account in accounts:
                if form.username.data == account['username']:
                    flash("This username was taken. Please try again" ,category='username_error')
                    return redirect(url_for("signup"))
            
            
            new_account = {
                'firstname': form.firstname.data,
                'lastname': form.lastname.data,
                'emailaddress': form.email.data,
                'username': form.username.data,
                'password': form.password.data,
                'followers': [],
                'following': []
            }
            
            accounts.append(new_account)
            with open('app/static/accounts.json', 'w') as all_accounts:
                dump(accounts, all_accounts, indent=4, sort_keys=True)

            return redirect(url_for('login')) 
    return render_template('signup.html',form=form)
    

# @app.route('/account')
# def account():

#     return render_template('account.html')

def get_num_followers(username):
    for account in accounts:
        if account['username'] == session.get('username'):
            return len(account['followers'])
def get_num_following(username):
    for account in accounts:
        if account['username'] == session.get('username'):
            return len(account['following'])

@app.route('/account', methods=['GET','POST'])
def account():
    username = session.get('username')
    myposts = []
    with open('app/static/accounts.json', 'r') as accounts_file:
            accounts = load(accounts_file)
    with open('app/static/posts.json', 'r') as posts_file:
        posts = load(posts_file)
    for account in accounts:
        if username == account['username']:


            global usernameinfo
            usernameinfo = account['username']
            global firstnameinfo
            firstnameinfo = account['firstname']
            global lastnameinfo
            lastnameinfo = account['lastname']
            global emailinfo
            emailinfo = account['emailaddress']
    
    for post in posts:
        if username == post['author']:
            myposts.append(post['image'])



    return render_template('account.html', usernamei=usernameinfo, firstnamei=firstnameinfo, lastnamei=lastnameinfo,
                           emaili=emailinfo, username=session.get('username'), postsi = myposts, num_followers=get_num_followers(session.get('username')), num_following=get_num_following(session.get('username')))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('timeline'))

if __name__ == '__main__':
    app.run(debug=True)