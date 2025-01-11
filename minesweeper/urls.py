from django.urls import path

from . import views
from .views import IndexView, GameView

app_name = 'minesweeper'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("game/<str:difficulty>", GameView.as_view(), name="game"),
]