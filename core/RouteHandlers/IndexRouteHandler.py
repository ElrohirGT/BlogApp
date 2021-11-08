from django.shortcuts import render

class IndexRouteHandler():
    def GetResponse(request):
        return render(request, "index.html")