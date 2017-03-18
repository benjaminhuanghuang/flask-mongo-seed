from flask import Blueprint

api = Blueprint('from . import authentication, posts, users, comments, errorsapi', __name__)
from . import  errors