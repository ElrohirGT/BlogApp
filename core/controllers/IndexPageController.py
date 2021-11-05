from django.shortcuts import render

class IndexPageController():
    def GetResponse(request):
        return render(request, "index.html")