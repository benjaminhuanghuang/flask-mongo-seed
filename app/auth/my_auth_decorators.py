import functools
from flask import current_app, abort
from flask_login import current_user
from permission import Permission


def login_required(func):
    '''
    decorate check use is authenticated before calling the actual view.
    It is a sample, I did not use it in project yet.
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        skip_login = current_app.config.get('LOGIN_DISABLED', current_app.config.get('TESTING', False))
        if skip_login:
            return func(*args, **kwargs)
        elif not current_app.login_manager.is_current_user_authenticated():
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return wrapper


def permission_required(permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def admin_required(func):
    return permission_required(Permission.ADMINISTER)(func)
