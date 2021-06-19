from flask import Flask

def create_app():
    app = Flask(__name__)
    #for encryption purposes
    app.config["SECRET_KEY"] = "kdfdlkfdkdfd"

    return app