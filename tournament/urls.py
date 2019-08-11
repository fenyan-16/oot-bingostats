from django.urls import path
from . import views

urlpatterns = [
    # ex: /events/

    # ex: /tournaments/
    path('<format>', views.tournament_list, name='tournament-list'),
    path('new/<format>', views.tournament_new, name='tournament-new'),
    path('<int:tournament_id>/', views.tournament_detail, name='tournament-detail'),
    path('<int:tournament_id>/report', views.tournament_report, name='tournament-report'),
    path('<int:tournament_id>/bracket/new', views.bracket_new, name='bracket-new'),
    path('<int:tournament_id>/bracket', views.showbracket, name='tournament-bracket'),
    path('<int:tournament_id>/seeding', views.showseeding, name='tournament-seeding'),
    path('<int:tournament_id>/participants', views.showparticipants, name='tournament-participants'),


    # path('tournaments/new/', views.tournament_new, name='tournament-new'),
    # path('<int:tournament_id>/seeding', views.tournament_seeding, name='tournament-seeding'),

]