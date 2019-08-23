from django.urls import path
from . import views

urlpatterns = [
    path('edit', views.profile_edit, name='league-new'),
    path('signup/', views.signup, name='signup'),
    path('<int:user_id>/', views.profile_detail, name='league-detail'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/', views.activate_account, name='activate'),
    path('activate/(?P<token>[0-9A-Za-z]{1,13}', views.activate_account, name='activate'),
    path('activate/-[0-9A-Za-z]{1,20})/$', views.activate_account, name='activate'),
]