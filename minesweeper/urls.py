from django.urls import path

from . import views
from .views import IndexView, GameView, ChooseDifficultyView

app_name = 'minesweeper'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("game/", ChooseDifficultyView.as_view(), name="choose_difficulty"),
    path("game/<str:difficulty>", GameView.as_view(), name="game"),
]