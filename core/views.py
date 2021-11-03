from django import forms
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .forms import CreateUserForm, LogInUserForm
from .models import User
import os
import hashlib

ENCRIPTING_ITERATIONS = 10**6 #Minimum recommended is 100,000

def EncryptPassword(password, passwordSalt = os.urandom(32)):
    return (hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        passwordSalt,
        ENCRIPTING_ITERATIONS), passwordSalt)

# Create your views here.
def register_user(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
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
        form = CreateUserForm()
        return render(request, "index.html", {"form":form})
    return HttpResponseNotFound()

def login_user(request):
    if request.session.__contains__("User"):
        return HttpResponseRedirect("../")
    elif request.method=="GET":
        form = LogInUserForm()
        return render(request, "login.html", {"form":form})
    elif request.method=="POST":
        form = LogInUserForm(request.POST)
        if not form.is_valid():
            messages.error(request, "The username or password are incorrect!")
            return HttpResponseRedirect(request.path)

        matchingUsers = User.objects.filter(Email=form.cleaned_data["NameOrEmail"])
        if matchingUsers.count() == 0:
            matchingUsers = User.objects.filter(Name=form.cleaned_data["NameOrEmail"])
        if matchingUsers.count() == 0:
            messages.error(request, "The username or password are incorrect!")
            return HttpResponseRedirect(request.path)

        user = matchingUsers[0]
        (password, _) = EncryptPassword(form.cleaned_data["Password"], user.Salt)
        if user.Password != password:
            messages.error(request, "The username or password are incorrect!")
            return HttpResponseRedirect(request.path)
        request.session["UserId"] = user.pk
        return  HttpResponse("Logged in!")

    return HttpResponseNotFound()