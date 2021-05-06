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
                similarity = self.__get_genre_similarity(game, user_activity_game)
                page_visit_score = self.__get_page_visit_scores(activity)
                delta = self.__get_delta(activity, user_activity_game)
                score = (similarity + page_visit_score) * delta
                max_score += score
            game_scores[game] = max_score
        return game_scores

    def __get_delta(self, activity, user_activity_game):
        today = datetime.datetime.today()
        days_since_last_activity = (today - activity.last_update).total_seconds() / 60 / 60 / 24
        positive_proportion = \
            user_activity_game.num_of_positive_reviews / (user_activity_game.num_of_positive_reviews + user_activity_game.num_of_negative_reviews)
        return (1/(1+days_since_last_activity) + positive_proportion)/2

    def __get_page_visit_scores(self, activity):
        page_visit_score = activity.page_entries + activity.steam_store_visits * 2
        return page_visit_score

    def __get_genre_similarity(self, game1, game2):
        similarity = 0
        for genre1 in game1.genres:
            for genre2 in game2.genres:
                if genre1.name == genre2.name:
                    similarity += 1
        return similarity/float(len(game1.genres) + len(game2.genres))

    def __get_game_by_id(self, id):
        for game in self.games:
            if game.id == id:
                return game
        return None
