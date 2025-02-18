from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from minesweeper.models import Game, Highscore
from minesweeper.game.minesweepergame import MinesweeperGame
from minesweeper.config import DIFFICULTY_BEGINNER, DIFFICULTY_INTERMEDIATE, DIFFICULTY_EXPERT

class MinesweeperGameTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_game_creation(self):
        game = MinesweeperGame(player=self.user, difficulty=DIFFICULTY_BEGINNER, width=9, height=9, mine_count=10)
        self.assertEqual(game.width, 9)
        self.assertEqual(game.height, 9)
        self.assertEqual(game.mine_count, 10)
        self.assertEqual(game.difficulty, DIFFICULTY_BEGINNER)
        self.assertFalse(game.game_over)
        self.assertFalse(game.game_won)

    def test_game_logic_board(self):
        game = MinesweeperGame(player=self.user, difficulty=DIFFICULTY_BEGINNER, width=9, height=9, mine_count=10)
        self.assertEqual(len(game.logic_board), 9)
        self.assertEqual(len(game.logic_board[0]), 9)
        self.assertEqual(sum(row.count(-1) for row in game.logic_board), 10)

    def test_game_user_board(self):
        game = MinesweeperGame(player=self.user, difficulty=DIFFICULTY_BEGINNER, width=9, height=9, mine_count=10)
        self.assertEqual(len(game.user_board), 9)
        self.assertEqual(len(game.user_board[0]), 9)
        self.assertTrue(all(cell == 'c' for row in game.user_board for cell in row))

    def test_game_cell_left_click(self):
        game = MinesweeperGame(player=self.user, difficulty=DIFFICULTY_BEGINNER, width=9, height=9, mine_count=10)
        game.cell_left_clicked(0, 0)
        self.assertNotEqual(game.user_board[0][0], 'c')

    def test_game_cell_right_click(self):
        game = MinesweeperGame(player=self.user, difficulty=DIFFICULTY_BEGINNER, width=9, height=9, mine_count=10)
        game.cell_right_clicked(0, 0)
        self.assertEqual(game.user_board[0][0], 'f')
        game.cell_right_clicked(0, 0)
        self.assertEqual(game.user_board[0][0], 'c')

    def test_game_win_condition(self):
        game = MinesweeperGame(player=self.user, difficulty=DIFFICULTY_BEGINNER, width=9, height=9, mine_count=10)
        for y in range(9):
            for x in range(9):
                if game.logic_board[y][x] != -1:
                    game.cell_left_clicked(y, x)
        self.assertTrue(game.game_over)
        self.assertTrue(game.game_won)

    def test_game_lose_condition(self):
        game = MinesweeperGame(player=self.user, difficulty=DIFFICULTY_BEGINNER, width=9, height=9, mine_count=10)
        for y in range(9):
            for x in range(9):
                if game.logic_board[y][x] == -1:
                    game.cell_left_clicked(y, x)
                    break
        self.assertTrue(game.game_over)
        self.assertFalse(game.game_won)


class HighscoreTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.game = Game.objects.create(
            player=self.user,
            difficulty=DIFFICULTY_BEGINNER,
            width=9,
            height=9,
            mine_count=10,
            logic_board=[[0] * 9 for _ in range(9)],
            user_board=[['c'] * 9 for _ in range(9)],
            traversed_board=[[False] * 9 for _ in range(9)],
            time_started="2023-01-01T00:00:00Z",
            time_spent=1000,
            time_ended="2023-01-01T00:00:01Z",
            game_over=True,
            game_won=True,
            seed="testseed"
        )
        self.highscore = Highscore.objects.create(game=self.game)

    def test_highscore_creation(self):
        self.assertEqual(self.highscore.game, self.game)

class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_index_view(self):
        response = self.client.get(reverse('minesweeper:index'))
        self.assertEqual(response.status_code, 200)

    def test_highscores_view(self):
        response = self.client.get(reverse('minesweeper:highscores'))
        self.assertEqual(response.status_code, 200)

    def test_choose_difficulty_view(self):
        response = self.client.get(reverse('minesweeper:choose_difficulty'))
        self.assertEqual(response.status_code, 200)

    def test_game_view(self):
        response = self.client.get(reverse('minesweeper:game', args=[DIFFICULTY_BEGINNER]))
        self.assertEqual(response.status_code, 200)