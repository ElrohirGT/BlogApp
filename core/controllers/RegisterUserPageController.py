from django.contrib import messages
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render

from core.controllers.PackageMethods import EncryptPassword
from core.forms import RegisterForm
from core.models import User

class RegisterUserPageController():

    def GetResponse(request):
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
            return render(request, "register.html", {"form":form})
        return HttpResponseNotFound()