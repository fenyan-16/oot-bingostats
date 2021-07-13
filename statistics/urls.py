from django.urls import path
from . import views

urlpatterns = [
    # ex: /events/

    # ex: /tournaments/

    path('<int:year>/goals/<str:phase>', views.goals, name='goals'),
    path('<int:year>/players/<str:phase>', views.players, name='players'),
    path('<int:year>/combinations/', views.combinations, name='combinations'),
	path('frequency/', views.frequency, name='frequency'),


    # path('tournaments/new/', views.tournament_new, name='tournament-new'),
    # path('<int:tournament_id>/seeding', views.tournament_seeding, name='tournament-seeding'),

]