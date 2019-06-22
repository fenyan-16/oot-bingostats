from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from events import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', include('events.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),
]