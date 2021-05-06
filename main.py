# main.py

from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from recommender import Recommender
from .models import Game, UserActivity
from . import db

main = Blueprint('main', __name__)

recommender = Recommender()


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/shop')
@login_required
def shop():
    games = Game.query.all()
    user_activity = UserActivity.query.filter_by(user_id=current_user.id)
    suggested_games = recommender.recommend(user_activity, games, 4)
    return render_template('shop.html', games=games, suggested_games=suggested_games)


@main.route('/product/<id>')
@login_required
def product(id):
    game = Game.query.filter_by(app_id=id).first()
    num_of_activites_for_current_user = UserActivity.query.filter_by(user_id=current_user.id, game_id=game.id).count()
    if num_of_activites_for_current_user == 0:
        user_activity = UserActivity(user_id=current_user.id, game_id=game.id)
        db.session.add(user_activity)
        db.session.commit()
    user_activity = UserActivity.query.filter_by(user_id=current_user.id, game_id=game.id).first()
    user_activity.page_entries += 1
    user_activity.last_update = db.func.now()
    db.session.commit()
    return render_template('product.html', game=game)


@main.route('/product_steam_page/<id>')
@login_required
def product_steam_page(id):
    game = Game.query.filter_by(app_id=id).first()
    num_of_activites_for_current_user = UserActivity.query.filter_by(user_id=current_user.id, game_id=game.id).count()
    if num_of_activites_for_current_user == 0:
        user_activity = UserActivity(user_id=current_user.id, game_id=game.id)
        db.session.add(user_activity)
        db.session.commit()
    user_activity = UserActivity.query.filter_by(user_id=current_user.id, game_id=game.id).first()
    user_activity.steam_store_visits += 1
    user_activity.last_update = db.func.now()
    db.session.commit()
    return redirect("https://store.steampowered.com/app/{}".format(id))