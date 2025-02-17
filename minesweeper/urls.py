from django.urls import path

from . import views
from .views import IndexView, GameView, ChooseDifficultyView, HighscoresView

app_name = 'minesweeper'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("highscores/", HighscoresView.as_view(), name="highscores"),
    path("game/", ChooseDifficultyView.as_view(), name="choose_difficulty"),
    path("game/<str:difficulty>", GameView.as_view(), name="game"),
]