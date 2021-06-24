from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

# Creating object for database integration
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    # for encryption purposes
    app.config["SECRET_KEY"] = "kdfdlkfdkdfd"
    # setting up database
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)  # associate database with our app

    # registering blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Initialize/Create Database
    from .models import User, Note  # load our schema(s)
    create_database(app)

    # manage Login related information
    login_manager = LoginManager()
    # redirect user here if NOT logged in
    login_manager.login_view = "auth.login"
    login_manager.init_app(app=app)
    login_manager.login_message = "You need to be Logged In first!"
    login_manager.login_message_category = "error"

    # Load a user using his/her id
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("wesite/" + DB_NAME):
        db.create_all(app=app)
        print("Database Created!")
