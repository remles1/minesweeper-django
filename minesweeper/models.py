from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    width = models.IntegerField()
    height = models.IntegerField()
    mine_count = models.IntegerField()
    logic_board = models.JSONField()  # where the bombs are
    user_board = models.JSONField()  # how to present the board in frontend (user interacts with this field)
    traversed_board = models.JSONField()  # used in algorithms. Stored to speed things up
    time = models.IntegerField()  # time it took for user to win the game (in ms)
    is_over = models.BooleanField()  # is the game still being played?
    is_won = models.BooleanField()  # is the game lost or won?

    def __str__(self):
        return f"pk={self.pk}, logic_board={self.logic_board}"