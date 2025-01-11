from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", include("django_registration.backends.one_step.urls")),
    path("", include("django.contrib.auth.urls")),
    path('index/', views.Index.as_view(), name='index'),
    path('profile/', views.AccountProfile.as_view(), name='account_profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')

]