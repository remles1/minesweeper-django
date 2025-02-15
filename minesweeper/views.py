import os

from django.views.generic import TemplateView

from minesweeper.config import difficulty_mapping
from mysite import settings


class IndexView(TemplateView):
    template_name = "minesweeper/index.html"


class GameView(TemplateView):
    template_name = "minesweeper/game.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        difficulty = self.kwargs.get('difficulty')

        if difficulty not in ["beginner", "intermediate", "expert"]:
            difficulty = "beginner"

        context['difficulty_settings'] = difficulty_mapping[difficulty]

        return context


class ChooseDifficultyView(TemplateView):
    template_name = "minesweeper/choose_difficulty.html"

