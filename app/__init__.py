from flask import Flask
from flask_mail import Mail

from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo

from config import config

mail = Mail()

mongo = PyMongo()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # flask ext init
    mail.init_app(app)  # read app.config to mail
    login_manager.init_app(app)
    bootstrap.init_app(app)

    mongo.init_app(app)

    # init routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    return app
