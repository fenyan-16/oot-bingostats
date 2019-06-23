from django.urls import path
from . import views

urlpatterns = [
    # ex: /events/
    path('', views.eventlist, name='eventlist'),
    path('myevents/', views.myevents, name='myevents'),
    # ex: /events/5/
    path('<int:event_id>/', views.event_detail, name='detail'),
    path('new/', views.event_new, name='event-new'),
    path('<int:event_id>/edit/', views.event_edit, name='event-edit'),
    path('<int:event_id>/register/', views.event_register, name='event-register'),
    path('<int:event_id>/register/status', views.event_registration_status, name='event-registration-status'),

    # ex: /tournaments/
    path('<int:event_id>/<int:tournament_id>/', views.tournamentdetail, name='tournament-detail'),
    path('<int:event_id>/tournaments/', views.EventsByUserListView.as_view(), name='event-tournaments'),
    path('<int:event_id>/tournaments/new/', views.tournament_new, name='tournament-new'),

    # Phases
    path('<int:event_id>/<int:tournament_id>/phase/new/', views.phase_new, name='phase-new'),
]