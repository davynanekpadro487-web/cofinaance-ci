from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/credits/', include('credits.urls')),
    path('api/assurance/', include('assurance.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/support/', include('support.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger-ui'),
    path('chat/', TemplateView.as_view(
        template_name='support/chat.html'
    ), name='chat'),
    path('', TemplateView.as_view(
        template_name='frontend/login.html'), 
        name='login'),
    path('dashboard/', TemplateView.as_view(
        template_name='frontend/dashboard.html'), 
        name='dashboard'),
    path('credits/', TemplateView.as_view(
        template_name='frontend/credits.html'), 
        name='credits'),
    path('assurance/', TemplateView.as_view(
        template_name='frontend/assurance.html'), 
        name='assurance_frontend'),
    path('notifications/', TemplateView.as_view(
        template_name='frontend/notifications.html'), 
        name='notifications_frontend'),
    path('profil/', TemplateView.as_view(
        template_name='frontend/profil.html'), 
        name='profil'),
]
