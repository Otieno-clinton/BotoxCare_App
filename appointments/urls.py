from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]
