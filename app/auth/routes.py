from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from . import auth

from user import validate_username_password, create_user, is_user_existed
from .forms import LoginForm, RegisterForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = validate_username_password(form.email.data, form.password.data)
        if user:
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        if is_user_existed(user_name):
            flash('Invalid username or password.')
        else:
            user = create_user(user_name, password)
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('auth/signup.html', form=form)
