from flask import render_template, redirect, url_for
from . import main
from app.auth.auth_decorators import *

@main.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html', title="Home")


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="Home")
