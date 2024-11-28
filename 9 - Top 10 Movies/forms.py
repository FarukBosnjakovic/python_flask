from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class FindMovieForm(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired()]) 
    submit = SubmitField(label='Add Movie')
    

class RateMovieForm(FlaskForm):
    rating = StringField('You rating Out of 10')
    review = StringField('Your review')
    submit = SubmitField('Done')
    