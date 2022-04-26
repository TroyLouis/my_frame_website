from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, ValidationError, DataRequired

class NewsletterSignup(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')