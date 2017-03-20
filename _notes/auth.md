
---------------
[*] What happened when user access a url/page


[*] What happened when user login by using from
    
    1. Get user name and password from web request
    
    2. Query data base to validate user name and password
    
    3. If step 2 is successful, save user id into session and redirect user to the next url or home page
       if need remember user, save a tag in session.
       
    4. If step 2 failed, redirect user to login page/view
    

[*] "Remember me" works

[*] Support OpenID

[*] Support various database
    Provide load_user callback function.
    It is used to load user object from database by using the userid stored in session.
    @login_manager.user_loader
    def load_user(userid):
        return User.get(userid)
    reload_user() will call it when it is necessary

Documents
---------------
    * Flask-Login doc
        
        https://flask-login.readthedocs.io/en/latest/
    
        http://www.pythondoc.com/flask-login/
    
    * Flask-Login github
    
        https://github.com/maxcountryman/flask-login/
    
    * Build a User Login System With Flask-Login, Flask-WTForms, Flask-Bootstrap, and Flask-SQLAlchemy
        
        https://www.youtube.com/watch?v=8aTnmsDMldY&t=22s


    * How to use MongoDB (and PyMongo) with Flask-Login
      
      https://runningcodes.net/flask-login-and-mongodb/


Logging for tracing
---------------
