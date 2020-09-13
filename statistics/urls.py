from django.urls import path
from . import views

urlpatterns = [
    # ex: /events/

    # ex: /tournaments/

    path('goals', views.goals, name='goals'),
	path('goals_top16', views.goals_t16, name='goals_top16'),
    path('players', views.players, name='players'),
	path('players_top16', views.players_t16, name='players_top16'),
	path('players_rebalance', views.players_rebalance, name='players_rebalance'),
    path('combinations', views.combinations, name='combinations'),
	path('frequency', views.frequency, name='frequency'),


    # path('tournaments/new/', views.tournament_new, name='tournament-new'),
    # path('<int:tournament_id>/seeding', views.tournament_seeding, name='tournament-seeding'),

]