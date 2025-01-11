from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'index.html'


class AccountProfile(TemplateView):
    template_name = 'account_profile.html'
