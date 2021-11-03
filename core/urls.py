from django.urls import path
from . import views

urlpatterns = [
    path("", views.register_user),
    path("login/", views.login_user)
]
