from django.contrib import admin
from .models import ClinicAdmin

class ClinicAdminAdmin(admin.ModelAdmin):
    list_display = ("user", "clinic_name", "is_active")
    search_fields = ("clinic_name", "user__username")
    list_filter = ("is_active",)

admin.site.register(ClinicAdmin, ClinicAdminAdmin)
