from django.urls import path
from .views import (
    NotificationListView,
    MarquerLuView,
    MarquerToutLuView
)

urlpatterns = [
    path('', NotificationListView.as_view(),
         name='notifications_list'),
    path('<int:pk>/lire/', MarquerLuView.as_view(),
         name='marquer_lu'),
    path('tout-lire/', MarquerToutLuView.as_view(),
         name='marquer_tout_lu'),
]
