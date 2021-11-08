import datetime
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from core.RouteHandlers.PackageMethods import CheckSession, SendErrors

from core.forms import ArticleForm
from core.models import Article, User

WORD_READING_SPEED = 300 #words per minute
class ArticleEditorRouteHandler():
    def GetResponse(request):
        if not CheckSession(request):
            return HttpResponseRedirect("/login")
        
        userId = request.session["UserId"]

        if request.method == "POST":
            form = ArticleForm(request.POST)
            if not form.is_valid():
                SendErrors(request, form.errors)
                return HttpResponseRedirect(request.path)
            article = form.save(commit=False)
            wordCount = 0
            for line in article.Body.html:
                wordCount += len(line.split())
            article.ReadTime = datetime.time(0, int(wordCount / WORD_READING_SPEED), 0)
            article.Author = User.objects.get(pk=userId)
            article.save()
            return HttpResponseRedirect("/dashboard")
            

        article = Article()
        if request.GET.__contains__("articleId"):
            articleId = request.GET["articleId"]
            if Article.objects.filter(pk=articleId).filter(Author__pk=userId).exists():
                article = Article.objects.get(pk=articleId)
        
        form = ArticleForm(instance=article)
        return render(request, "articleEditor.html", {"form":form})