from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Email


class LoginForm(Form):
    email = StringField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegisterForm(Form):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Sign up')
