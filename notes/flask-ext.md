pip install flask-bootstrap
----------------------

from flask.ext.bootstrap import Bootstrap
# ...
bootstrap = Bootstrap(app)

In template
{% extends "bootstrap/base.html" %}

The base template from Flask-Bootstrap provides a skeleton web page that includes all the 
Bootstrap CSS and JavaScript files.

pip install flask-moment
----------------------
    Flask-Moment depends on jquery.js in addition to moment.js
