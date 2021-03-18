# 
# This file contains custom form classes for the instagram replica.
#
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, InputRequired, Email, Length

class CommentForm(FlaskForm):
    comment = TextAreaField('comment', render_kw={"placeholder": "Add a comment...", "id": "comment-textarea"}, validators = [Required()])
    parentID = HiddenField('uuid')
    author = HiddenField('author')



class Register(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    email = EmailField('email', validators=[InputRequired(), Email()])
    firstname = StringField('firstname', validators=[InputRequired()])
    lastname = StringField('lastname', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired(), Length(max=18,min=6)])
    #submit = SubmitField('Submit')


class Login(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    #submit = SubmitField('Submit')