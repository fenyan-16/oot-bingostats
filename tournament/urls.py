from django.urls import path
from . import views

urlpatterns = [
    # ex: /events/

    # ex: /tournaments/
    path('<int:tournament_id>/', views.tournamentdetail, name='tournament-detail'),
    path('<int:tournament_id>/bracket', views.showbracket, name='tournament-bracket'),
    path('new', views.tournament_new, name='tournament-new'),
    # path('tournaments/new/', views.tournament_new, name='tournament-new'),
    # path('<int:tournament_id>/seeding', views.tournament_seeding, name='tournament-seeding'),

]