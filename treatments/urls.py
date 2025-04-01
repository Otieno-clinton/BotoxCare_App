from django.urls import path
from . import views

urlpatterns = [
    path("treatments/", views.treatment_list, name="treatment_list"),
    path("treatments/<int:treatment_id>/", views.treatment_detail, name="treatment_detail"),
]
