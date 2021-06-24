from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

"""
We have one-to-many relationship from `User -> Note`
i.e. 1 user(parent) can have many notes(children)
"""


class User(db.Model, UserMixin):
    # Defining User schema

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # store "notes"(in some sort of list) associated to the "user"
    notes = db.relationship("Note")


class Note(db.Model):
    # Defining Note schema
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10_000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # foreign key referring to primary key of `User`
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
