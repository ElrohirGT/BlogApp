from django.urls import path
from core.controllers.ArticleDetailsPageController import ArticleDetailsPageController
from core.controllers.ArticleEditorPageController import ArticleEditorPageController

from core.controllers.IndexPageController import IndexPageController
from core.controllers.LogInPageController import LogInPageController
from core.controllers.RegisterUserPageController import RegisterUserPageController
from core.controllers.UserDashboardController import UserDashboardController

urlpatterns = [
    path("", IndexPageController.GetResponse),
    path("register/", RegisterUserPageController.GetResponse),
    path("login/", LogInPageController.GetResponse),
    path("dashboard/", UserDashboardController.GetResponse),
    path("articleEditor/", ArticleEditorPageController.GetResponse),
    path("article/<int:articleId>", ArticleDetailsPageController.GetResponse)
]
