from werkzeug.security import check_password_hash
from bson import ObjectId
from app import db_client, login_manager
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
    u = db_client.db['users'].find_one({"user_name": user_name})
    if not u or not check_password_hash(u["password"], password):
        return None
    return User(u)

@login_manager.user_loader
def load_user(user_id):
    u = db_client.db['users'].find_one({"_id": ObjectId(user_id)})
    if not u:
        return None
    user = User(u)
    return user