#app folder for our instagram app, will contain app routes for traversing
#through the application

import json
#code to start application
from datetime import datetime
from os import path
from uuid import uuid4

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_wtf import FlaskForm
from jinja2 import Environment
from wtforms import PasswordField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, InputRequired, Length
from wtforms_components import validators

from applib.app_lib import (follow, get_accounts, get_num_followers,
                            get_num_following, get_posts, get_profile_pic,
                            like_post, post_comment,
                            set_profile_pic, swap_theme, unfollow, unlike_post,
                            auth_login, post_a_picture, create_account)
from applib.forms import (Colormode, CommentForm, Follow, Like, Login,
                          Register, Unfollow, Unlike)

jinja_env = Environment() 


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config['SECRET_KEY'] = 'ErenYeager'


@app.route("/", methods=['GET','POST'])
@app.route("/timeline", methods=['GET','POST'])
def timeline():
    form = CommentForm(request.form)
    follow_form = Follow(request.form)
    unfollow_form = Unfollow(request.form)
    like_form = Like(request.form)
    unlike_form = Unlike(request.form)
    color_mode_form = Colormode(request.form)
    posts = get_posts()
    accounts = get_accounts()
    if request.method == 'POST':
        if form.validate_on_submit():
            if 'comment' in request.form:
                comment = form.comment.raw_data[0]
                parentID = form.parentID.raw_data[0]
                author = form.author.raw_data[0]
                post_comment(parentID, {'author': author, 'comment': comment})
            return redirect(url_for('timeline'))
            
        if 'follow_user' in request.form:
            follow(session.get('username'), request.form.get('follow_user'))
            return redirect(url_for('timeline'))
        if 'unfollow_user' in request.form:
            unfollow(session.get('username'), request.form.get('unfollow_user'))
            return redirect(url_for('timeline'))
        if 'like_post_uuid' in request.form:
            like_post(session.get('username'), request.form.get('like_post_uuid'))
            return redirect(url_for('timeline'))
        if 'unlike_post_uuid' in request.form:
            unlike_post(session.get('username'), request.form.get('unlike_post_uuid'))
            return redirect(url_for('timeline'))
        if 'color_mode' in request.form:
            swap_theme('timeline')
    return render_template('timeline.html', posts=posts, form=form, username=session.get('username'), accounts=accounts, follow_form=follow_form, unfollow_form=unfollow_form, like_form=like_form, unlike_form=unlike_form, color_mode_form=color_mode_form, color_theme=session.get('color_theme'))

#posting feature


@app.route("/posting", methods=['GET','POST'])
def image_post():
    color_mode_form = Colormode(request.form)
    posts = get_posts()
    if request.method == 'POST':
        if 'color_mode' in request.form:
            swap_theme('image_post')
        elif 'description' in request.form:
            poster_name = session.get('username')
            date = datetime.today().strftime("%d/%m/%Y")
            
            img_file = request.files['file']
            description = request.form['description']

            if img_file.filename == "":
                print("No file selected")
                return redirect(url_for('image_post'))

            file_path = path.join(app.root_path, 'static/images', img_file.filename)
            img_file.save(file_path)

            new_post = {
                "uuid": str(uuid4()),
                "author": poster_name,
                "description": description,
                "image": img_file.filename,
                "date_posted": date,
                "comments": list(),
                "likers": list()
            }

            post_a_picture(new_post)

            return redirect(url_for('timeline'))
    return render_template('posting.html', posts=posts, username=session.get('username'), color_mode_form=color_mode_form, color_theme=session.get('color_theme'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login()
    color_mode_form = Colormode(request.form)
    posts = get_posts()
    if request.method == 'POST':
        if 'color_mode' in request.form:
                swap_theme('login')
        if form.validate_on_submit():
            if auth_login(form.username.data, form.password.data):
                session['username'] = form.username.data
                flash(session['username'] + " is logged in", category='username is logged in')
                return redirect(url_for('timeline'))
            else:
                flash("The username or password you entered is incorrect." , category='loginerror')
    return render_template("login.html", form=form, posts=posts, color_mode_form=color_mode_form, color_theme=session.get('color_theme'))

@app.route("/register",methods=['POST','GET'])
def signup():
    form = Register()
    color_mode_form = Colormode(request.form)
    accounts = get_accounts()
    if request.method == 'POST':
        if 'color_mode' in request.form:
                swap_theme('signup')
    if request.method == 'POST':
        if form.validate_on_submit():
            for account in accounts:
                if form.username.data == account['username']:
                    flash("This username is taken. Please try again", category='username_error')
                    return redirect(url_for("signup"))

            new_account = {
                'firstname': form.firstname.data,
                'lastname': form.lastname.data,
                'emailaddress': form.email.data,
                'username': form.username.data,
                'password': form.password.data,
                'followers': list(),
                'following': list(),
                'profile_pic': 'avatar.png'
            }

            create_account(new_account)
            
            return redirect(url_for('login')) 

    return render_template('signup.html',form=form, color_mode_form=color_mode_form, color_theme=session.get('color_theme'))        

@app.route('/account', methods=['POST','GET'])
def account():
    color_mode_form = Colormode(request.form)
    posts = get_posts()
    username = session.get('username')
    myposts = list()
    pic_name = ''

    if request.method == 'POST':
        if 'color_mode' in request.form:
            swap_theme('account')
        if 'img' in request.files:

            img_f = request.files['img']

            if img_f.filename == "":
                return redirect(url_for('account'))

            #getting the user profile picture name and filename
            file_path = path.join(app.root_path, 'static/images', img_f.filename) 
            img_f.save(file_path)
            set_profile_pic(session.get('username'), img_f.filename)

            #redirect to account function to load the new user profile picture in account.html
            return redirect(url_for('account')) 

    accounts = get_accounts()
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

    
    pic_name = get_profile_pic(session.get('username'))

    #getting and returning the user profile picture for the user in the session

    return render_template('account.html', mypicsi=pic_name,usernamei=usernameinfo, firstnamei=firstnameinfo, lastnamei=lastnameinfo,
                    emaili=emailinfo, username=session.get('username'), postsi = myposts, num_followers=get_num_followers(session.get('username')), num_following=get_num_following(session.get('username')), color_mode_form=color_mode_form, color_theme=session.get('color_theme'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('timeline')) 

if __name__ == '__main__':
    app.run(debug=True)
