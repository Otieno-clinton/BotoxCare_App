from django.urls import path
from . import views

urlpatterns = [
    path('treatments/', views.api_treatments, name='api_treatments'),
    path('appointments/', views.api_appointments, name='api_appointments'),
]
