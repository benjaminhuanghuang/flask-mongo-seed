import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_USERNAME = "ben.email.sender@gmail.com"
    MAIL_PASSWORD = "1@11@11@1"

    DB_SERVER_URI = ""



class DevelopmentConfig(Config):
    DEBUG = True



class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DATABASE_URI = ""


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

