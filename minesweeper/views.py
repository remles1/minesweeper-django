import os

from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import Http404
from django.views.generic import TemplateView

from minesweeper.config import difficulty_mapping, DIFFICULTY_BEGINNER, DIFFICULTY_INTERMEDIATE, DIFFICULTY_EXPERT, \
    HIGHSCORES_PER_PAGE, HIGHSCORE_CACHE_TIMEOUT
from minesweeper.models import Highscore
from mysite import settings


class IndexView(TemplateView):
    template_name = "minesweeper/index.html"


class HighscoresView(TemplateView):
    template_name = "minesweeper/highscores.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        highscores = cache.get('cached_highscores')
        if highscores is None:
            beginner = Highscore.objects.filter(game__difficulty=DIFFICULTY_BEGINNER).select_related('game').order_by(
                'game__time_spent')
            intermediate = Highscore.objects.filter(game__difficulty=DIFFICULTY_INTERMEDIATE).select_related(
                'game').order_by('game__time_spent')
            expert = Highscore.objects.filter(game__difficulty=DIFFICULTY_EXPERT).select_related('game').order_by(
                'game__time_spent')

            paginator_beginner = Paginator(beginner, HIGHSCORES_PER_PAGE)
            paginator_intermediate = Paginator(intermediate, HIGHSCORES_PER_PAGE)
            paginator_expert = Paginator(expert, HIGHSCORES_PER_PAGE)

            page_beginner = self.request.GET.get(DIFFICULTY_BEGINNER)
            page_intermediate = self.request.GET.get(DIFFICULTY_INTERMEDIATE)
            page_expert = self.request.GET.get(DIFFICULTY_EXPERT)

            highscores = {DIFFICULTY_BEGINNER: paginator_beginner.get_page(page_beginner),
                          DIFFICULTY_INTERMEDIATE: paginator_intermediate.get_page(page_intermediate),
                          DIFFICULTY_EXPERT: paginator_expert.get_page(page_expert)}

            cache.set('cached_highscores', highscores, timeout=HIGHSCORE_CACHE_TIMEOUT)

        context['highscores'] = highscores

        return context


class GameView(TemplateView):
    template_name = "minesweeper/game.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        difficulty = self.kwargs.get('difficulty')

        if difficulty not in [DIFFICULTY_BEGINNER, DIFFICULTY_INTERMEDIATE, DIFFICULTY_EXPERT]:
            raise Http404("Invalid difficulty")

        context['difficulty_settings'] = difficulty_mapping[difficulty]

        return context


class ChooseDifficultyView(TemplateView):
    template_name = "minesweeper/choose_difficulty.html"

