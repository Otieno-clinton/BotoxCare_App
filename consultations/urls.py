from django.urls import path
from . import views

urlpatterns = [
    path('consultationlist', views.consultation_list, name='consultation_list'),
    path("consultations/", views.virtual_consultations, name="virtual_consultations"),

    path('<int:id>/', views.consultation_detail, name='consultation_detail'),
    path("consultation/<int:consultation_id>/waiting/", views.waiting_room, name="waiting_room"),
    path("consultation/<int:consultation_id>/video/", views.start_video_call, name="start_video_call"),
]
