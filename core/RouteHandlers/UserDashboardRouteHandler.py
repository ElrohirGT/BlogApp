from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from core.RouteHandlers.PackageMethods import CheckSession

from core.models import Article

class UserDashboardRouteHandler():
    def GetResponse(request):
        if not CheckSession(request):
            return HttpResponseRedirect("/login")

        userId = request.session["UserId"]
        articles = list(Article.objects.filter(Author__id=userId))
        
        context = {
            "UserName": request.session["UserName"],
            "UserArticles": articles
        }
        return render(request, "dashboard.html", context)