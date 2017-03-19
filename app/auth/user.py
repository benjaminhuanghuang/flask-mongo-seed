from werkzeug.security import check_password_hash
from bson import ObjectId
from app import db_client
from permission import Permission


class User():
    def __init__(self, u):
        self.u = u
        self.user_name = u["user_name"]
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
        p = user_permission(self.role)
        return (p & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


def user_permission(role):
    roles = {
        'user': Permission.READ,
        'tutor': (Permission.READ | Permission.WRITE | Permission.DELETE),
        'admin': (0xff)
    }
    return roles.get(role, roles["user"])


def user_login(user_name, password):
    u = db_client.db['users'].find_one({"user_name": user_name})
    if not u or not check_password_hash(u["password"], password):
        return None
    return User(u)


def load_user(user_id):
    u = db_client.db['users'].find_one({"_id": ObjectId(user_id)})
    if not u:
        return None
    user = User(u)
    return user

# current_app.login_manager.user_loader = load_user
