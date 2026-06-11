from django.urls import path
from .views import TableauDeBordView

urlpatterns = [
    path('', TableauDeBordView.as_view(), name='dashboard'),
]
