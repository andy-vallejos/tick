from django.urls import path
from .views import register, login, get_user, get_users

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("users/", get_users),
    path("users/<int:user_id>/", get_user)
]
