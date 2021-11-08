from django.contrib import messages
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render

from core.RouteHandlers.PackageMethods import EncryptPassword
from core.forms import LogInUserForm
from core.models import User

class LogInRouteHandler():
    def GetResponse(request):
        if request.session.__contains__("UserName"):
            return HttpResponseRedirect("/dashboard")
        if request.method=="GET":
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