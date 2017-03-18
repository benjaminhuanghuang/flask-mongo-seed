import functools
from flask import session, abort, flash, redirect, url_for
from flask.ext.login import current_user

from permission import Permission


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            # abort(403)
            flash('You need to login first.')
            return redirect(url_for('login'))

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
