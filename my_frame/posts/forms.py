from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    picture = FileField('Upload Image', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Submit')

class SetActiveForm(FlaskForm):
    submit = SubmitField('Set As Active')