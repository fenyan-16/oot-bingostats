from django.urls import path
from . import views

urlpatterns = [
    # ex: /events/

    # ex: /tournaments/

    path('goals', views.goals, name='goals'),
    path('players', views.players, name='players'),
    path('combinations', views.combinations, name='combinations'),
	path('frequency', views.frequency, name='frequency'),


    # path('tournaments/new/', views.tournament_new, name='tournament-new'),
    # path('<int:tournament_id>/seeding', views.tournament_seeding, name='tournament-seeding'),

]