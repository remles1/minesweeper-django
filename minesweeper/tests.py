from django.contrib.auth.models import User
from django.test import TestCase

from minesweeper.game.minesweepergame import MinesweeperGame


# Create your tests here.

class GameLogicTests(TestCase):
    logic_board_final = [
        -1, 2, 2, -1, 1,
        2, -1, 2, 1, 1,
        1, 1, 1, 0, 0,
        0, 0, 0, 1, 1,
        0, 0, 0, 1, -1,
    ]

    logic_board_only_mines = [
        -1, 0, 0, -1, 0,
        0, -1, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, -1,
    ]
    user_board_win = [
        "c", "2", "2", "c", "1",
        "2", "c", "2", "1", "1",
        "1", "1", "1", "0", "0",
        "0", "0", "0", "1", "1",
        "0", "0", "0", "1", "c",
    ]

    def test_count_mines_nearby(self):
        """
        count_mines_nearby() should return properly counted mines neighboring a cell
        given mines location

        """

        pass