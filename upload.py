# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
import http.client
import json

from .models import Game, Tag
from . import db


upload = Blueprint('upload', __name__)


@upload.route('/upload')  # TODO: this should be restricted
def upload_method():
    MAX_TO_COLLECT = 30

    api_client = http.client.HTTPSConnection("api.steampowered.com")
    store_client = http.client.HTTPSConnection("store.steampowered.com")

    appIds = []
    api_client.request("GET", "/ISteamApps/GetAppList/v2/")
    response = api_client.getresponse()
    byteData = response.read()
    answer = json.loads(byteData.decode("utf-8"))
    for app in answer["applist"]["apps"]:
        appIds.append(app["appid"])
    appIds.sort()

    print("Retrieved {} app ids".format(len(appIds)))

    answers = []
    review_answers = []
    for appId in appIds:
        try:
            store_client.request("GET", "/api/appdetails?appids={}".format(appId))
            response = store_client.getresponse()
            byteData = response.read()
            answer = json.loads(byteData.decode("utf-8"))
            store_client.request("GET", "/appreviews/{}?json=1".format(appId))
            response = store_client.getresponse()
            byteData = response.read()
            review_answer = json.loads(byteData.decode("utf-8"))
            if answer[str(appId)]["success"] and review_answer["success"] == 1:
                if answer[str(appId)]["data"]["type"] == "game":  # filter games
                    answers.append(answer[str(appId)]["data"])
                    review_answers.append(review_answer["query_summary"])
            if len(answers) >= MAX_TO_COLLECT:
                break
        except Exception as e:
            print(e)

    app_ids = []  # this is needed for special cases, which cause duplicate ids
    for answer, review_answer in zip(answers, review_answers):
        if answer["steam_appid"] not in app_ids:
            new_game = Game(name=answer["name"], description=answer["about_the_game"],
                            header_image_url=answer["header_image"],
                            price=0 if "price_overview" not in answer else answer["price_overview"]["final"],
                            price_currency="" if "price_overview" not in answer else answer["price_overview"]["currency"],
                            app_id=answer["steam_appid"],
                            num_of_positive_reviews=review_answer["total_positive"],
                            num_of_negative_reviews=review_answer["total_negative"])
            db.session.add(new_game)
            tags = [category["description"] for category in answer["categories"]]
            for tag_name in tags:
                new_tag = Tag(app_id=answer["steam_appid"], name=tag_name)
                db.session.add(new_tag)
            app_ids.append(answer["steam_appid"])
    db.session.commit()

    return "Done"
