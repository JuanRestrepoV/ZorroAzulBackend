from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib import admin
from django.urls import path
from users.views import *

urlpatterns = [
    path(r'api/login/', LoginView.as_view()),
    path(r'api/register/', RegisterView.as_view()),
    path(r'api/profile/', ProfileView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

