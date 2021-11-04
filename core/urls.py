from django.urls import path
from . import views

urlpatterns = [
    path("", views.register_user),
    path("login/", views.login_user),
    path("dashboard/", views.user_dashboard),
    path("articleEditor/", views.article_editor),
    path("articles/", views.article)
]
