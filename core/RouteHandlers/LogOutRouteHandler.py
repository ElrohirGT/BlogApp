from django.http.response import HttpResponseRedirect

from core.RouteHandlers.PackageMethods import CheckSession

class LogOutRouteHandler:
    def GetResponse(request):
        if CheckSession(request):
            del request.session["UserName"]
        return HttpResponseRedirect("/")
