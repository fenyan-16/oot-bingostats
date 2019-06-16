from django.urls import path

from . import views

urlpatterns = [
    # ex: /events/
    path('', views.index, name='index'),
    # ex: /events/5/
    path('<int:event_id>/', views.detail, name='detail'),

    # ex: /tournaments/5/
    path('<int:event_id>/<int:tournament_id>/', views.tournamentdetail, name='tournament-detail'),
    path('myevents/', views.EventsByUserListView.as_view(), name='my-events'),
    path('<int:event_id>/tournaments/', views.EventsByUserListView.as_view(), name='event-tournaments'),
]