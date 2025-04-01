from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.clinic_admin_dashboard, name="clinic_admin_dashboard"),
    path("specialists/approve/<int:specialist_id>/", views.approve_specialist, name="approve_specialist"),
    path("specialists/suspend/<int:specialist_id>/", views.suspend_specialist, name="suspend_specialist"),
    path("appointments/", views.manage_appointments, name="manage_appointments"),

    path("register/", views.clinic_admin_register, name="clinic_admin_register"),
    path("login/", views.clinic_admin_login, name="clinic_admin_login"),
    path("logout/", views.clinic_admin_logout, name="clinic_admin_logout"),
    path("edit-clinic/", views.edit_clinic_details, name="edit_clinic_details"),
    path("add-specialist/", views.add_specialist, name="add_specialist"),

    path("appointments/assign/<int:appointment_id>/", views.assign_specialist, name="assign_specialist"),
]
