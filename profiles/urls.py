from django.urls import path
from . import views
from django.conf.urls import re_path

urlpatterns = [
    path('<int:user_id>/edit', views.profile_edit, name='profile-edit'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('<int:user_id>/', views.profile_detail, name='profile-datail'),
    path('<slug:user_name>/', views.profile_detail_name, name='profile-datail_name'),
    re_path(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]