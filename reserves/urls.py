from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path(r'api/Reserves/', ReservesView.as_view()),
]