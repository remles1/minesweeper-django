from django.urls import path

from .views import IndexView, GameView, ChooseDifficultyView, HighscoresView, InstructionsView, about

app_name = 'minesweeper'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("instructions/", InstructionsView.as_view(), name="instructions"),
    path("about/", about, name="about"),
    path("highscores/", HighscoresView.as_view(), name="highscores"),
    path("game/", ChooseDifficultyView.as_view(), name="choose_difficulty"),
    path("game/<str:difficulty>", GameView.as_view(), name="game"),
]