#app folder for our instagram app, will contain app routes for traversing
#through the application

#code to start application
from datetime import datetime
from json import load, dump
from flask import Flask, render_template, request, url_for, redirect, flash, session
from os import path
from uuid import uuid4
from forms import CommentForm, Register, Login, Follow, Unfollow, Like, Unlike, Colormode
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length
from jinja2 import Environment
import json

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

def swap_theme(page):
    if session.get('color_theme'):
        if session.get('color_theme') == 'dark':
            session['color_theme'] = 'light'
            return redirect(url_for(page))
        if session.get('color_theme') == 'light':
            session['color_theme'] = 'dark'
            return redirect(url_for(page))
    session['color_theme'] = 'light'
    return redirect(url_for(page))

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

def like_post(person_liking, post_uuid):
    for post in posts:
        if post['uuid'] == post_uuid:
            if person_liking not in post['likers']:
                post['likers'].append(person_liking)
                break
            else:
                break
    with open('app/static/posts.json', 'w') as all_posts:
        dump(posts, all_posts, indent=4, sort_keys=True)

def unlike_post(person_unliking, post_uuid):
    for post in posts:
        if post['uuid'] == post_uuid:
            if person_unliking in post['likers']:
                post['likers'].remove(person_unliking)
                break
            else:
                break
    with open('app/static/posts.json', 'w') as all_posts:
        dump(posts, all_posts, indent=4, sort_keys=True)



@app.route("/", methods=['GET','POST'])
@app.route("/timeline", methods=['GET','POST'])
def timeline():
    form = CommentForm(request.form)
    follow_form = Follow(request.form)
    unfollow_form = Unfollow(request.form)
    like_form = Like(request.form)
    unlike_form = Unlike(request.form)
    color_mode_form = Colormode(request.form)
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
        if 'like_post_uuid' in request.form:
            like_post(session.get('username'), request.form.get('like_post_uuid'))
        if 'unlike_post_uuid' in request.form:
            unlike_post(session.get('username'), request.form.get('unlike_post_uuid'))
        if 'color_mode' in request.form:
            swap_theme('timeline')
    return render_template('timeline.html', posts=posts, form=form, username=session.get('username'), accounts=accounts, follow_form=follow_form, unfollow_form=unfollow_form, like_form=like_form, unlike_form=unlike_form, color_mode_form=color_mode_form, color_theme=session.get('color_theme'))

#posting feature
@app.route("/posting", methods=['GET', 'POST'])
def post():
    color_mode_form = Colormode(request.form)
    if request.method == 'POST':
        if 'color_mode' in request.form:
                swap_theme('post')
    return render_template('posting.html', posts=posts, username=session.get('username'), color_mode_form=color_mode_form, color_theme=session.get('color_theme'))


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
    new_post['num_likes'] = 0

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
    color_mode_form = Colormode(request.form)
    if request.method == 'POST':
        if 'color_mode' in request.form:
                swap_theme('login')
    if form.validate_on_submit():
        if valid(form.username.data, form.password.data):
            username = form.username.data
            session['username'] = form.username.data
            flash(username + " is logged in",category='username is logged in')
            return redirect(url_for('timeline'))
        else:
            flash("Your USERNAME/PASSWORD might be incorrect!" , category='loginerror')
    return render_template("login.html", form=form, posts=posts, color_mode_form=color_mode_form, color_theme=session.get('color_theme'))

@app.route("/register",methods=['POST','GET'])
def signup():
    form = Register()
    color_mode_form = Colormode(request.form)
    if request.method == 'POST':
        if 'color_mode' in request.form:
                swap_theme('signup')
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
            
            #from here, a default user profile picture (Avatar.png) will be added to all new users
            accounts.append(new_account)
            with open('app/static/accounts.json', 'w') as all_accounts:
                dump(accounts, all_accounts, indent=4, sort_keys=True)

            new_profile_pic = {'username' : form.username.data, 'pic_URl' : 'Avatar.png'}

            with open('app/static/profile_pic.json', 'r') as pics:
                all_profile_pics = load(pics)
                
            all_profile_pics.append(new_profile_pic)
            with open('app/static/profile_pic.json', 'w') as all_pics:
                dump(all_profile_pics, all_pics, indent=4, sort_keys=True) #saving the user profile picture to the user indicated in profile_pic.json
                all_pics.close
                
            return redirect(url_for('login')) 
    return render_template('signup.html',form=form, color_mode_form=color_mode_form, color_theme=session.get('color_theme'))
    

def get_num_followers(username):
    for account in accounts:
        if account['username'] == session.get('username'):
            return len(account['followers'])
def get_num_following(username):
    for account in accounts:
        if account['username'] == session.get('username'):
            return len(account['following'])

@app.route('/account', methods=['POST','GET'])
def account():
    color_mode_form = Colormode(request.form)
    if request.method == 'POST':
        if 'color_mode' in request.form:
                swap_theme('account')
    username = session.get('username')
    myposts = []
    pic_name = ''
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

    
    with open('app/static/profile_pic.json', 'r') as profile_pics:
        pics = load(profile_pics)
    
        for pic in pics:
            if pic['username'] == session.get('username'):
                pic_name = pic['pic_URl']

    #getting and returning the user profile picture for the user in the session
        if request.method == 'POST':
            img_f = request.files['img']

            if img_f.filename == "":
                return redirect(url_for('account'))

            file_path = path.join(app.root_path, 'static/images', img_f.filename) #getting the user profile picture name and filename
            img_f.save(file_path)
            

            new_profile_pic = {} #creating a new dictionary to save the new user profile picture
            new_profile_pic['username'] = session.get('username')
            new_profile_pic['pic_URl']   = img_f.filename

            with open('app/static/profile_pic.json', 'r') as profile_pics:
                pics = load(profile_pics)

            with open('app/static/profile_pic.json', 'w') as all_pics: #replaccing the old user profile picture with the new user profile picture
                for pic in pics:
                    if pic['username'] == session.get('username'):
                        pic['pic_URl'] = img_f.filename
                        dump(pics, all_pics, indent=4, sort_keys=True)
                        all_pics.close()
            return redirect(url_for('account')) #redirect to account function to load the new user profile picture in account.html

        return render_template('account.html', mypicsi=pic_name,usernamei=usernameinfo, firstnamei=firstnameinfo, lastnamei=lastnameinfo,
                    emaili=emailinfo, username=session.get('username'), postsi = myposts, num_followers=get_num_followers(session.get('username')), num_following=get_num_following(session.get('username')), color_mode_form=color_mode_form, color_theme=session.get('color_theme'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('timeline')) 

if __name__ == '__main__':
    app.run(debug=True)