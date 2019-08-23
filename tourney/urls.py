from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
# from events import views

urlpatterns = [

    path('', include('tournament.urls')),
    path('events/', include('events.urls')),
    path('admin/', admin.site.urls),
    path('tournaments/', include('tournament.urls')),
    path('leagues/', include('leagues.urls')),
    # path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', include('profiles.urls')),
    # path('profile/edit', views.update_profile, name='profile-edit'),
]