# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.user_create),
    path('login/', views.login_api),
]
