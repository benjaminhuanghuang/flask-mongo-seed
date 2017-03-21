from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Email


class LoginForm(Form):
    email = StringField('UserName', validators=[InputRequired(), Length(3, 15)])  # , Email()
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegisterForm(Form):
    username = StringField('UserName', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=3, max=20)])
    submit = SubmitField('Sign up')
