from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from accounts.models import ProfileModel


class Index(TemplateView):
    template_name = 'index.html'


class AccountProfile(TemplateView):
    template_name = 'account_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        player = self.request.user

        profile = ProfileModel.objects.get(player=player)

        context['profile'] = profile
        return context
