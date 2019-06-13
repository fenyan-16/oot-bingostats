from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the tourney index.")

def detail(request, event_id):
    return HttpResponse("You're looking at question %s." % event_id)