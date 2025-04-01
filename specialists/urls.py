from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import approve_appointment, decline_appointment, specialist_profile

urlpatterns = [
    path('dashboard/', views.dashboard, name='specialist_dashboard'),
    path("login/", views.specialist_login, name="specialist_login"),
    path('profile/<int:specialist_id>/', views.specialist_profile, name='specialist_profile'),
    path('appointments/', views.manage_appointments, name='specialist_appointments'),
    path("appointments/approve/<int:appointment_id>/", views.approve_appointment, name="approve_appointment"),
    path("appointments/decline/<int:appointment_id>/", views.decline_appointment, name="decline_appointment"),
    path('appointments/', views.appointment_list, name='confirm'),
    path('consultations/', views.consultations, name='specialist_consultations'),
    path('reviews/', views.reviews, name='specialist_reviews'),
    path('payments/', views.payments, name='specialist_payments'),
    # path('support/', views.support, name='specialist_support'),
    path('register/', views.specialist_register, name='specialist_register'),

    path('logout/', LogoutView.as_view(), name='specialist_logout'),

]
