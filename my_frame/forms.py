from flask_wtf import FlaskForm
from my_frame.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),Length(min=1,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=1)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another username!')

    def validate_email(self, email):
        email_address = User.query.filter_by(email=email.data.lower()).first()
        if email_address:
            raise ValidationError(f"That email is already in use. Please use another email address or login.")

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=1)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),Length(min=1,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another username!')

    def validate_email(self, email):
        if email.data != current_user.email:
            email_address = User.query.filter_by(email=email.data.lower()).first()
            if email_address:
                raise ValidationError(f"That email is already in use. Please use another email address or login.")

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    picture = FileField('Upload Image', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Post Image')