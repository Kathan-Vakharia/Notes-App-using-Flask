# contains authentication routes for the application
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.helpers import get_flashed_messages
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User

auth = Blueprint("auth", __name__)

"""A note about which HTTP Request is made
GET - When the page is requested at that url
POST - When the form is submitted on that url
"""


@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # get(name) where name is the value of 'name' attribute of input box
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        """Flashing
        The flashing system basically makes it possible to record a 
        message at the end of a request and access it next request 
        and only next request.
        In simple words, you can use the "get_flashed_messages()"
        method exactly once after a message is flashed

        """
        user = User.query.filter_by(email=email).first()
        # maintain uniqueness of email addresses
        if user and user.is_active:
            flash("This email address is taken, if it is you then login else use a different one!",
                  category="error")
        # input validation
        elif len(email) < 4:
            flash("Email must be greater than 3 characters", category="error")

        elif len(first_name) < 2:
            flash("first name must be greater than 1 character", category="error")

        elif len(password1) < 7:
            flash("Password must be atleast 7 characters", category="error")

        elif password1 != password2:
            flash("Both passwords don't match!", category="error")

        else:
            # add user to database
            new_usr = User(email=email, first_name=first_name,
                           password=generate_password_hash(password1,
                                                           method="sha256")
                           )
            db.session.add(new_usr)
            db.session.commit()

            flash("Account created!", category="success")
            login_user(user=new_usr, remember=True)  # login the user

            # redirect user to home page
            return redirect(url_for("views.home")  # returns URL for views.home("/")
                            )

    return render_template("sign_up.html", user=current_user)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                login_user(user=user, remember=True)  # login the user
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect Password, Try Again", category="error")
        else:
            flash("Email is not registered, please SignUp ", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()  # logs out and deletes `remember`
    return redirect(url_for("auth.login"))
