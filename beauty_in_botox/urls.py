from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("core.urls")),
    path('Clients/', include('Clients.urls')),
    path('treatments/', include('treatments.urls')),
    path('appointments/', include('appointments.urls')),
    path('payments/', include('payments.urls')),
    path("consultations/", include("consultations.urls")),
    path('reviews/', include('reviews.urls')),
    path('admin-panel/', include('admin_panel.urls')),
    path('api/', include('api.urls')),  # For API integration
    path('specialists/', include('specialists.urls')),
    path('clinic_admins/', include('clinic_admins.urls')),
]
