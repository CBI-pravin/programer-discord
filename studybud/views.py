from socket import fromshare


from django.http import HttpResponse




def home(request):
    return HttpResponse(request)