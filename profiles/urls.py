from django.urls import path
from . import views

urlpatterns = [
    path('edit', views.profile_edit, name='league-new'),
    path('signup/', views.profile_detail, name='league-detail'),
    path('<int:user_id>/', views.profile_detail, name='league-detail'),
]