from django import forms
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .forms import ArticleForm, RegisterForm, LogInUserForm
from .models import Article, User
import os
import hashlib
import datetime

ENCRIPTING_ITERATIONS = 10**6 #Minimum recommended is 100,000
ONE_CHARACTER_READING_TIME = 0.01 #seconds per char

def EncryptPassword(password, passwordSalt = os.urandom(32)):
    return (hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        passwordSalt,
        ENCRIPTING_ITERATIONS), passwordSalt)

def SendErrors(errors):
    for error in errors:
        messages.error(error)

# Create your views here.
def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Please write valid information!")
            return HttpResponseRedirect(request.path)

        user = User()
        user.Name = form.cleaned_data["Name"]
        user.Email = form.cleaned_data["Email"]
        (encryptedPassword, salt) = EncryptPassword(form.cleaned_data["Password"])
        user.Password = encryptedPassword
        user.Salt = salt

        user.save()
        return HttpResponseRedirect("/login")
    elif request.method=="GET":
        form = RegisterForm()
        return render(request, "index.html", {"form":form})
    return HttpResponseNotFound()

def login_user(request):
    if request.session.__contains__("UserName"):
        return HttpResponseRedirect("/dashboard")
    elif request.method=="GET":
        form = LogInUserForm()
        return render(request, "login.html", {"form":form})
    elif request.method=="POST":
        form = LogInUserForm(request.POST)
        if not form.is_valid():
            messages.error(request, "The username or password were incorrect!")
            return HttpResponseRedirect(request.path)

        matchingUsers = User.objects.filter(Email=form.cleaned_data["NameOrEmail"])
        if matchingUsers.count() == 0:
            matchingUsers = User.objects.filter(Name=form.cleaned_data["NameOrEmail"])
        if matchingUsers.count() == 0:
            messages.error(request, "The username or password were incorrect!")
            return HttpResponseRedirect(request.path)

        user = matchingUsers[0]
        (password, _) = EncryptPassword(form.cleaned_data["Password"], user.Salt)
        if user.Password != password:
            messages.error(request, "The username or password were incorrect!")
            return HttpResponseRedirect(request.path)
        
        request.session["UserId"] = user.pk
        request.session["UserName"] = user.Name
        return  HttpResponseRedirect("/dashboard")

    return HttpResponseNotFound()

def user_dashboard(request):
    if not request.session.__contains__("UserName"):
        return HttpResponseRedirect("/login")

    userId = request.session["UserId"]
    articles = list(Article.objects.filter(Author__id=userId))
    
    context = {
        "UserName": request.session["UserName"],
        "UserArticles": articles
    }
    return render(request, "dashboard.html", context)

def article_editor(request):
    if not request.session.__contains__("UserName"):
        return HttpResponseRedirect("/login")
    
    userId = request.session["UserId"]

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if not form.is_valid():
            SendErrors(form.errors)
            return HttpResponseRedirect(request.path)
        article = form.save(commit=False)
        numberOfCharacters = 0
        for line in article.Body.html:
            numberOfCharacters += len(line)
        article.ReadTime = datetime.time(0, 0, int(numberOfCharacters * ONE_CHARACTER_READING_TIME))
        article.Author_id = userId
        article.save()
        

    article = Article()
    if request.GET.__contains__("articleId"):
        articleId = request.GET["articleId"]
        if Article.objects.filter(pk=articleId).filter(Author__pk=userId).exists():
            article = Article.objects.get(pk=articleId)
    
    form = ArticleForm(instance=article)
    return render(request, "articleEditor.html", {"form":form})

def article(request):
    if not request.method == "GET" or not request.GET.__contains__("articleId"):
        return HttpResponseRedirect("/")
    articleId = request.GET["articleId"]
    if not Article.objects.filter(pk=articleId).exists():
        return HttpResponseRedirect("/")
    
    article = Article.objects.get(pk=articleId)
    return render(request, "articleDetails.html", {"Article":article})