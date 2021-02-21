# 
# This file contains custom form classes for the instagram replica.
#
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, TextAreaField
from wtforms.validators import Required

class CommentForm(FlaskForm):
    comment = TextAreaField('comment', render_kw={"placeholder": "Add a comment...", "id": "comment-textarea"}, validators = [Required()])
    parentID = HiddenField('uuid')
    author = HiddenField('author')