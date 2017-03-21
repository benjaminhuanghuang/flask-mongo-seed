from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_required, login_user, logout_user
from . import auth

from app.utilities import is_safe_url
from user import validate_username_password, create_user, is_user_existed
from .forms import LoginForm, RegisterForm

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        if is_user_existed(user_name):
            flash('User name is existed.')
        else:
            user = create_user(user_name, password)
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.dashboard'))
    return render_template('auth/signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = validate_username_password(form.email.data, form.password.data)
        if user:
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('main.dashboard'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)



@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))