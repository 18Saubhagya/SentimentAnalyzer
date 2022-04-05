from django.contrib import admin
from django.urls import path
from . import views
import requests, sys

urlpatterns = [
    path('', views.input, name='input'),
    path('analyze', views.analyze, name='analyze'),
]