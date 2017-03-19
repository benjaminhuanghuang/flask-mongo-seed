'''
    Based on flask_login.py
'''
from flask import abort, current_app, flash, redirect, request, session, url_for
from flask import _request_ctx_stack, has_request_context

from urlparse import urlparse, urlunparse
from werkzeug.urls import url_decode, url_encode

#: The default flash message to display when users need to log in.
LOGIN_MESSAGE = u'Please log in to access this page.'

#: The default flash message category to display when users need to log in.
MESSAGE_CATEGORY = 'message'

#: The default flash message to display when users need to reauthenticate.
REFRESH_MESSAGE = u'Please reauthenticate to access this page.'


class LoginManager(object):
    '''
    This object is used to hold the settings used for logging in. Instances of
    :class:`LoginManager` are *not* bound to specific apps, so you can create
    one in the main body of your code and then bind it to your
    app in a factory function.
    '''

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        '''
        Configures an application. This registers an `after_request` call, and
        attaches this `LoginManager` to it as `app.login_manager`.

        :param app: The :class:`flask.Flask` object to configure.
        :type app: :class:`flask.Flask`
        :param add_context_processor: Whether to add a context processor to
            the app that adds a `current_user` variable to the template.
            Defaults to ``True``.
        :type add_context_processor: bool
        '''
        app.login_manager = self

    def unauthorized(self):
        if not self.login_view:
            abort(401)

        flash(LOGIN_MESSAGE, category=MESSAGE_CATEGORY)

        return redirect(login_url(self.login_view, request.url))

    def is_current_user_authenticated(self):
        pass

    def is_current_user_can(self, permission):
        pass


def login_user(user_id, pwd, remember=False):
    '''
    Logs a user in. You should pass the actual user object to this. If the
    user's `is_active` method returns ``False``, they will not be logged in
    unless `force` is ``True``.

    This will return ``True`` if the log in attempt succeeds, and ``False`` if
    it fails (i.e. because the user is inactive).

    :param user: The user object to log in.
    :type user: object
    :param remember: Whether to remember the user after their session expires.
        Defaults to ``False``.
    :type remember: bool
    :param force: If the user is inactive, setting this to ``True`` will log
        them in regardless. Defaults to ``False``.
    :type force: bool
    '''

    return True


def logout_user():
    '''
    Logs a user out. (You do not need to pass the actual user.) This will
    also clean up the remember me cookie if it exists.
    '''
    if 'user_id' in session:
        session.pop('user_id')

    if '_fresh' in session:
        session.pop('_fresh')

    cookie_name = current_app.config.get('REMEMBER_COOKIE_NAME', COOKIE_NAME)
    if cookie_name in request.cookies:
        session['remember'] = 'clear'

    user = _get_user()
    if user is not None and not user.is_anonymous():
        user_logged_out.send(current_app._get_current_object(), user=user)

    current_app.login_manager.reload_user()
    return True


def login_url(login_view, next_url=None, next_field='next'):
    '''
    Creates a URL for redirecting to a login page. If only `login_view` is
    provided, this will just return the URL for it. If `next_url` is provided,
    however, this will append a ``next=URL`` parameter to the query string
    so that the login view can redirect back to that URL.

    :param login_view: The name of the login view. (Alternately, the actual
                       URL to the login view.)
    :type login_view: str
    :param next_url: The URL to give the login view for redirection.
    :type next_url: str
    :param next_field: What field to store the next URL in. (It defaults to
                       ``next``.)
    :type next_field: str
    '''
    if login_view.startswith(('https://', 'http://', '/')):
        base = login_view
    else:
        base = url_for(login_view)

    if next_url is None:
        return base
    # parse url to
    # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    parts = list(urlparse(base))
    md = url_decode(parts[4])
    md[next_field] = make_next_param(base, next_url)
    parts[4] = url_encode(md, sort=True)
    return urlunparse(parts)


def make_next_param(login_url, current_url):
    '''
    Reduces the scheme and host from a given URL so it can be passed to
    the given `login` URL more efficiently.

    :param login_url: The login URL being redirected to.
    :type login_url: str
    :param current_url: The URL to reduce.
    :type current_url: str
    '''
    l = urlparse(login_url)
    c = urlparse(current_url)

    if (not l.scheme or l.scheme == c.scheme) and \
            (not l.netloc or l.netloc == c.netloc):
        return urlunparse(('', '', c.path, c.params, c.query, ''))
    return current_url
