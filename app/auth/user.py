from werkzeug.security import check_password_hash, generate_password_hash
from bson import ObjectId
from app import mongo, login_manager
from permission import Permission
import base64

class User():
    def __init__(self, u):
        self.u = u
        self.username = u["user_name"]
        self.email = u["user_name"]
        self.role = u.get("role", "user")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.u["_id"])

    def can(self, permissions):
        p = role_to_permission(self.role)
        return (p & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


def role_to_permission(role):
    roles = {
        'user': Permission.READ,
        'tutor': (Permission.READ | Permission.WRITE | Permission.DELETE),
        'admin': (0xff)
    }
    return roles.get(role, roles["user"])


def validate_username_password(user_name, password):
    u = mongo.db['users'].find_one({"user_name": user_name})
    if not u or not check_password_hash(u["password"], password):
        return None
    return User(u)


def create_user(user_name, pwd):
    new_user = {
        "user_name": user_name,
        "password": generate_password_hash(pwd, method='pbkdf2:sha256')
    }
    _id = mongo.db['users'].insert(new_user)
    u = mongo.db['users'].find_one({"_id": _id})

    return User(u)

def is_user_existed(user_name):
    u = mongo.db['users'].find_one({"user_name": user_name})
    return u is not None


@login_manager.user_loader
def load_user(user_id):
    u = mongo.db['users'].find_one({"_id": ObjectId(user_id)})
    if not u:
        return None
    user = User(u)
    return user

#  support login from a url argument or from Basic Auth using the Authorization header
@login_manager.request_loader
def load_user_from_request(request):

    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None