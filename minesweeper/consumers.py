import json
import os

from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from minesweeper.config import difficulty_mapping
from minesweeper.game.minesweepergame import MinesweeperGame
from minesweeper.game.minesweeperstats import MinesweeperStats
from minesweeper.models import Game, GameStats


class GameConsumer(WebsocketConsumer):
    user: User
    game: MinesweeperGame
    game_stats: MinesweeperStats

    def connect(self):
        # session = self.scope["session"]
        # # Example: Check if user is authenticated
        # if self.scope['user'].is_authenticated:
        #     user = self.scope['user']  # Authenticated user
        #     self.accept()
        #     self.send(text_data=json.dumps({
        #         'message': f"Hello, {user.username}!"
        #     }))
        # else:
        #     self.close()  # Close the connection if not authenticated
        self.user = self.scope["user"]
        self.accept()
        self.start_a_new_game()
        self.send_user_board()

    def disconnect(self, close_code):
        pass
        # if self.game.game_over and self.game.game_won:
        #     model_game = Game(**vars(self.game))
        #     model_game.save()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json["type"] == "new_game":
            self.start_a_new_game()
            self.send_user_board()
            return

        message = text_data_json["message"]
        split_message = message.split('-')
        y = int(split_message[0])
        x = int(split_message[1])

        if text_data_json["type"] == "l_click":
            self.game.cell_left_clicked(y, x)

        if text_data_json["type"] == "r_click":
            self.game.cell_right_clicked(y, x)

        self.send_user_board()

        if self.game.game_over and self.game.game_won:
            self.calculate_stats()
            self.send_stats()
            if not self.user.is_anonymous:
                self.save_game_and_stats_to_db()

    def calculate_stats(self):
        self.game_stats = MinesweeperStats(self.game)

    def save_game_and_stats_to_db(self):
        model_game = Game(**vars(self.game))

        stats_dict = vars(self.game_stats).copy()

        stats_dict.pop('_traversed_board', None)

        stats_dict['game'] = model_game

        model_game_stats = GameStats(**stats_dict)

        model_game.save()
        model_game_stats.save()

    def send_user_board(self):
        user_board_json = json.dumps(self.game.user_board)
        self.send(text_data=json.dumps({
            "type": "user_board",
            "won": self.game.game_won,
            "over": self.game.game_over,
            "time": self.game.time_spent,
            "message": user_board_json
        })
        )

    def send_stats(self):
        stats_dict = vars(self.game_stats).copy()

        stats_dict.pop('game', None)
        stats_dict.pop('_traversed_board', None)

        stats_dict["time_spent"] = self.game.time_spent/1000  # time is send in seconds to the frontend
        self.send(text_data=json.dumps({
            "type": "game_stats",
            "message": f"{stats_dict}"
        }))

    def start_a_new_game(self):
        difficulty = self.scope['url_route']['kwargs']['difficulty']

        difficulty_settings = difficulty_mapping[difficulty]

        self.instantiate_minesweeper_game(difficulty_settings)

    def instantiate_minesweeper_game(self, difficulty_settings):
        self.game = MinesweeperGame(
            player=self.user,
            difficulty=difficulty_settings['name'],
            width=difficulty_settings['width'],
            height=difficulty_settings['height'],
            mine_count=difficulty_settings['mine_count'],
            seed=os.urandom(16).hex()
        )
