from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


def create_app():
    app= Flask(__name__)
    app.config["SECRET_KEY"]  = "SECRET"

    '''@app.route("/home")
    def home():
        return "<h1>HOME</h1>"'''
    
    '''. for relative import'''
    from .views import views
    from .auth import auth 

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app