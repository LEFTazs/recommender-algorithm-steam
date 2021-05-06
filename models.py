# models.py

from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    user_activity = db.relationship("UserActivity", backref="user", lazy=True)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    header_image_url = db.Column(db.String(200))
    price = db.Column(db.Integer())
    price_currency = db.Column(db.String(20))
    app_id = db.Column(db.Integer(), unique=True)
    num_of_positive_reviews = db.Column(db.Integer())
    num_of_negative_reviews = db.Column(db.Integer())
    genres = db.relationship("Genre", backref="game", lazy=True)
    user_activity = db.relationship("UserActivity", backref="game", lazy=True)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer(), db.ForeignKey('game.app_id'))
    name = db.Column(db.String(100))


class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer(), db.ForeignKey('game.id'))
    last_update = db.Column(db.DateTime(), server_default=db.func.now())
    page_entries = db.Column(db.Integer(), default=0)
    steam_store_visits = db.Column(db.Integer(), default=0)
