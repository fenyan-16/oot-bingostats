from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('edit', views.profile_edit, name='profile-edit'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('<int:user_id>/', views.profile_detail, name='profile'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]