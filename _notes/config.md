Flask + Mongo Project Setup
================

How to
--------------
* Create config.py in root folder

* Put config into app.config in __init__.py of app, 
    app = Flask(__name__)
    app.config.from_object(config[config_name])
     
Q&A
--------------
Why use config class instead of dictionary?
    1. Using class can create hierarchy of configuration classes