from django.contrib import admin
from django.urls import path
from users.views import *
from events.views import *

urlpatterns = [
    path(r'api/getEvents/', EventsView.as_view()),
    path(r'api/getAditionalServices/', AditionalServicesView.as_view()),
    path(r'api/getFloors/', FloorView.as_view()),
]