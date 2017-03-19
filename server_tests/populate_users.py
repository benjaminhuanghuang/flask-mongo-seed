from werkzeug.security import generate_password_hash
# from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from config import config


def main():
    # Connect to the DB
    mongo = MongoClient(config.get('MONGO_SERVER', "127.0.0.1"), config.get('MONGO_PORT', 27017))
    users_collection = mongo[config.get('DATABASE', "game_joy")]["users"]

    # Ask for data to store
    user = raw_input("Enter your username: ")
    password = raw_input("Enter your password: ")
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Insert the user in the DB
    try:
        users_collection.insert({"user_name": user, "password": pass_hash})
        print "User created."
    except DuplicateKeyError:
        print "User already present in DB."


if __name__ == '__main__':
    main()
