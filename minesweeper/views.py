from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import Http404
from django.views.generic import TemplateView

from minesweeper.config import difficulty_mapping, DIFFICULTY_BEGINNER, DIFFICULTY_INTERMEDIATE, DIFFICULTY_EXPERT, \
    HIGHSCORES_PER_PAGE, HIGHSCORE_CACHE_TIMEOUT
from minesweeper.models import Highscore, GameStats


class IndexView(TemplateView):
    template_name = "minesweeper/index.html"


class HighscoresView(TemplateView):
    template_name = "minesweeper/highscores.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cached_highscores = cache.get('cached_highscores')

        if cached_highscores is None:
            beginner = Highscore.objects.filter(game__difficulty=DIFFICULTY_BEGINNER).select_related(
                'game__player').order_by(
                'game__time_spent')
            beginner_stats = GameStats.objects.filter(game__in=beginner.values_list("game", flat=True))

            beginner_data = []
            for hs in beginner:
                stats = beginner_stats.filter(game=hs.game).first()
                beginner_data.append({
                    'highscore': hs,
                    'stats': stats
                })

            intermediate = Highscore.objects.filter(game__difficulty=DIFFICULTY_INTERMEDIATE).select_related(
                'game__player').order_by('game__time_spent')
            intermediate_stats = GameStats.objects.filter(game__in=intermediate.values_list("game", flat=True))

            intermediate_data = []
            for hs in intermediate:
                stats = intermediate_stats.filter(game=hs.game).first()
                intermediate_data.append({
                    'highscore': hs,
                    'stats': stats
                })

            expert = Highscore.objects.filter(game__difficulty=DIFFICULTY_EXPERT).select_related(
                'game__player').order_by(
                'game__time_spent')
            expert_stats = GameStats.objects.filter(game__in=expert.values_list("game", flat=True))

            expert_data = []
            for hs in expert:
                stats = expert_stats.filter(game=hs.game).first()
                expert_data.append({
                    'highscore': hs,
                    'stats': stats
                })

            cached_highscores = {
                DIFFICULTY_BEGINNER: beginner_data,
                DIFFICULTY_INTERMEDIATE: intermediate_data,
                DIFFICULTY_EXPERT: expert_data,
            }
            cache.set('cached_highscores', cached_highscores, timeout=HIGHSCORE_CACHE_TIMEOUT)

        page_beginner = self.request.GET.get(DIFFICULTY_BEGINNER, 1)
        page_intermediate = self.request.GET.get(DIFFICULTY_INTERMEDIATE, 1)
        page_expert = self.request.GET.get(DIFFICULTY_EXPERT, 1)

        paginator_beginner = Paginator(cached_highscores[DIFFICULTY_BEGINNER], HIGHSCORES_PER_PAGE)
        paginator_intermediate = Paginator(cached_highscores[DIFFICULTY_INTERMEDIATE], HIGHSCORES_PER_PAGE)
        paginator_expert = Paginator(cached_highscores[DIFFICULTY_EXPERT], HIGHSCORES_PER_PAGE)

        highscores = {
            DIFFICULTY_BEGINNER: paginator_beginner.get_page(page_beginner),
            DIFFICULTY_INTERMEDIATE: paginator_intermediate.get_page(page_intermediate),
            DIFFICULTY_EXPERT: paginator_expert.get_page(page_expert),
        }

        context['highscores'] = highscores
        context['DIFFICULTY_BEGINNER'] = DIFFICULTY_BEGINNER
        context['DIFFICULTY_INTERMEDIATE'] = DIFFICULTY_INTERMEDIATE
        context['DIFFICULTY_EXPERT'] = DIFFICULTY_EXPERT

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
