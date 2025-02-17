from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.TextField()
    width = models.IntegerField()
    height = models.IntegerField()
    mine_count = models.IntegerField()
    logic_board = models.JSONField()  # where the bombs are
    user_board = models.JSONField()  # how to present the board in frontend (user interacts with this field)
    traversed_board = models.JSONField()  # used in algorithms. Stored to speed things up
    time_started = models.DateTimeField()  # Date start game
    time_spent = models.FloatField()
    time_ended = models.DateTimeField(null=True)  # Date end game
    _cells_opened = models.IntegerField(null=True)
    game_over = models.BooleanField()  # is the game still being played?
    game_won = models.BooleanField()  # is the game lost or won?
    seed = models.TextField()

    def __str__(self):
        return f"pk={self.pk}, logic_board={self.logic_board}"


class GameStats(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tbv = models.IntegerField()
    tbv_per_second = models.FloatField()
    ios = models.FloatField()
    rqp = models.FloatField()


class Highscore(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
