from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, required


class search_game(Form):
    searchfield = StringField("Match ID", validators=[required()])
    submit = SubmitField("Submit")
