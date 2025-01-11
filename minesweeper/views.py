from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "minesweeper/index.html"


class GameView(TemplateView):
    template_name = "minesweeper/game.html"
    #extra_context = {"images": }


