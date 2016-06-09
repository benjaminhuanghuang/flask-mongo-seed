from flask import Flask
from flask.ext.login import LoginManager
from config import config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        config_name: the python path of the config object,
                     e.g. appname.settings.ProdConfig
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    if not app.config['DEBUG'] and not app.config['TESTING']:
        # configure logging for production

        # email errors to the administrators
        if app.config.get('MAIL_ERROR_RECIPIENT') is not None:
            import logging
            from logging.handlers import SMTPHandler
            credentials = None
            secure = None
            if app.config.get('MAIL_USERNAME') is not None:
                credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                if app.config['MAIL_USE_TLS'] is not None:
                    secure = ()

            # send log by email
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['MAIL_DEFAULT_SENDER'],
                toaddrs=[app.config['MAIL_ERROR_RECIPIENT']],
                subject='[Talks] Application Error',
                credentials=credentials,
                secure=secure)

            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # send standard logs to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

    login_manager.init_app(app)

    return app
