from django.urls import path
from . import views

urlpatterns = [
    # ex: /events/

    # ex: /tournaments/
    path('<int:tournament_id>/', views.tournamentdetail, name='tournament-detail'),
    path('<int:tournament_id>/bracket/new', views.bracket_new, name='bracket-new'),
    path('<int:tournament_id>/bracket', views.showbracket, name='tournament-bracket'),
    path('<int:tournament_id>/seeding', views.showseeding, name='tournament-seeding'),
    path('<int:tournament_id>/participants', views.showparticipants, name='tournament-participants'),
    path('new', views.tournament_new, name='tournament-new'),
    path('league', views.league, name='league-new'),
    # path('tournaments/new/', views.tournament_new, name='tournament-new'),
    # path('<int:tournament_id>/seeding', views.tournament_seeding, name='tournament-seeding'),

]