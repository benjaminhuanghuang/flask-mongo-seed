from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from . import auth

from user import validate_username_password
from .forms import LoginForm


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
