from pymongo import MongoClient


class DBClient(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.db = MongoClient(app.config.get('MONGO_SERVER', "127.0.0.1"),
                              app.config.get('MONGO_PORT', 27017))[app.config.get('DATABASE', "game_joy")]