import json

from channels.generic.websocket import WebsocketConsumer

from minesweeper.game.minesweepergame import MinesweeperGame


class GameConsumer(WebsocketConsumer):
    game: MinesweeperGame

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
        session = self.scope["session"]
        user = self.scope["user"]
        self.accept()

        self.game = MinesweeperGame(
            player=user,
            width=16,
            height=16,
            mine_count=40
        )
        user_board_json = json.dumps(self.game.user_board)
        self.send(text_data=json.dumps({
            "message": user_board_json
        }
        ))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        split_message = message.split('-')
        y = int(split_message[0])
        x = int(split_message[1])

        if text_data_json["btn"] == "l":
            self.game.cell_left_clicked(y, x)

        if text_data_json["btn"] == "r":
            self.game.cell_right_clicked(y, x)

        user_board_json = json.dumps(self.game.user_board)
        #print(user_board_json)
        self.send(text_data=json.dumps({
            "message": user_board_json
        }))
