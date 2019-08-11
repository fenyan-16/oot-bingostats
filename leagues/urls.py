from django.urls import path
from . import views

urlpatterns = [
    path('', views.league_list, name='league-list'),
    path('new', views.league_new, name='league-new'),
    path('<int:league_id>/', views.league_detail, name='league-detail'),
]