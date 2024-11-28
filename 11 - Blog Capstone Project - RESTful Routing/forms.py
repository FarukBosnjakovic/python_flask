from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField


class CreatePostForm(FlaskForm):
    title = StringField(label='Blog Post Title', validators=[DataRequired()])
    subtitle = StringField(label='Subtitle', validators=[DataRequired()])
    author = StringField(label='Your Name', validators=[DataRequired()])
    body = CKEditorField(label='Blog Content', validators=[DataRequired()]) 
    submit = SubmitField('Submit Post') 