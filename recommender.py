import datetime
import itertools
from collections import OrderedDict
from math import ceil


class Recommender:

    def __init__(self):
        self.games = []
        self.user_activity = []
        self.n = 0

    def recommend(self, user_activity, games, n):
        self.games = games
        self.user_activity = user_activity
        self.n = n

        game_scores = self.__calculate_scores_for_games()
        recommendations = self.__choose_n_best_games(game_scores)

        return recommendations

    def __choose_n_best_games(self, game_scores):
        sorted_game_scores = sorted(game_scores.items(), key=lambda x: x[1], reverse=True)
        return [score[0] for score in sorted_game_scores[:self.n]]

    def __calculate_scores_for_games(self):
        game_scores = {}
        for game in self.games:
            max_score = 0
            for activity in self.user_activity:
                user_activity_game = self.__get_game_by_id(activity.game_id)
                if user_activity_game.id == game.id:
                    continue
                positive_proportion = self.__get_review_score_for_game(user_activity_game)
                similarity = self.__get_tag_similarity(game, user_activity_game)
                delta = self.__get_delta_for_activity(activity)
                score = (similarity + delta) * positive_proportion
                if score > max_score:
                    max_score = score
            game_scores[game] = max_score
        return game_scores

    def __get_review_score_for_game(self, user_activity_game):
        positive_proportion = \
            user_activity_game.num_of_positive_reviews / (user_activity_game.num_of_positive_reviews + user_activity_game.num_of_negative_reviews)
        return positive_proportion

    def __get_delta_for_activity(self, activity):
        today = datetime.datetime.today()
        days_since_last_activity = ceil((today - activity.last_update).total_seconds()/60/60/24)
        delta = (1/days_since_last_activity) * (activity.page_entries + activity.steam_store_visits * 2)
        return delta

    def __get_tag_similarity(self, game1, game2):
        similarity = 0
        for tag1 in game1.tags:
            for tag2 in game2.tags:
                if tag1.name == tag2.name:
                    similarity += 1
        return similarity

    def __get_game_by_id(self, id):
        for game in self.games:
            if game.id == id:
                return game
        return None
