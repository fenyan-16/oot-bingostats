from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from .models import Event


def index(request):
    return HttpResponse("Hello, world. You're at the tourney index.")

def detail(request, event_id):
    return HttpResponse("You're looking at question %s." % event_id)


class EventsByUserListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'accounts/myevents.html'
    paginate_by = 10

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user).order_by('name')