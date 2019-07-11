from django.urls import path
from . import views

urlpatterns = [
    # ex: /events/

    # ex: /tournaments/
    path('test/', views.tournamentdetail, name='tournament-detail'),
    # path('tournaments/new/', views.tournament_new, name='tournament-new'),
    # path('<int:tournament_id>/seeding', views.tournament_seeding, name='tournament-seeding'),

]