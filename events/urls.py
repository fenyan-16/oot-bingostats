from django.urls import path
from . import views

urlpatterns = [
    # ex: /events/
    path('', views.eventlist, name='eventlist'),
    # ex: /events/5/
    path('<int:event_id>/', views.event_detail, name='detail'),
    path('new/', views.event_new, name='event-new'),

    # ex: /tournaments/5/
    path('<int:event_id>/<int:tournament_id>/', views.tournamentdetail, name='tournament-detail'),
    path('myevents/', views.myevents, name='myevents'),
    path('<int:event_id>/tournaments/', views.EventsByUserListView.as_view(), name='event-tournaments'),
    path('<int:event_id>/tournaments/new/', views.tournament_new, name='tournament-new'),
]