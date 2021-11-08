from django.urls import path

from core.RouteHandlers.ArticleDetailsRouteHandler import ArticleDetailsRouteHandler
from core.RouteHandlers.ArticleEditorRouteHandler import ArticleEditorRouteHandler
from core.RouteHandlers.IndexRouteHandler import IndexRouteHandler
from core.RouteHandlers.LogInRouteHandler import LogInRouteHandler
from core.RouteHandlers.RegisterUserRouteHandler import RegisterUserRouteHandler
from core.RouteHandlers.UserDashboardRouteHandler import UserDashboardRouteHandler
from core.RouteHandlers.LogOutRouteHandler import LogOutRouteHandler

urlpatterns = [
    path("", IndexRouteHandler.GetResponse),
    path("register/", RegisterUserRouteHandler.GetResponse),
    path("login/", LogInRouteHandler.GetResponse),
    path("dashboard/", UserDashboardRouteHandler.GetResponse),
    path("articleEditor/", ArticleEditorRouteHandler.GetResponse),
    path("article/<int:articleId>", ArticleDetailsRouteHandler.GetResponse),
    path("logout/", LogOutRouteHandler.GetResponse)
]
