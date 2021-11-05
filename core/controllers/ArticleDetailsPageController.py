from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from core.controllers.PackageMethods import SendErrors

from core.forms import CommentForm
from core.models import Article, Comment

class ArticleDetailsPageController():
    def GetResponse(request, articleId):
        if not Article.objects.filter(pk=articleId).exists():
            return HttpResponseRedirect("/")

        if request.method=="POST" and request.session.__contains__("UserName"):
            form = CommentForm(request.POST)
            if not form.is_valid():
                SendErrors(request, form.errors)
                return HttpResponseRedirect(request.path)
            comment = form.save(commit=False)
            comment.Author_id = request.session["UserId"]
            comment.Article_id = articleId
            comment.save()
        
        context = {
            "Article": Article.objects.get(pk=articleId),
            "IsLoggedIn": request.session.__contains__("UserName"),
            "CommentForm": CommentForm(),
            "Comments": list(Comment.objects.filter(Article__pk=articleId))
        }
        return render(request, "articleDetails.html", context)