from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import ClinicAdmin
from specialists.models import Specialist
from appointments.models import Appointment

# Clinic Admin Role Check
def clinic_admin_required(user):
    return ClinicAdmin.objects.filter(user=user, is_active=True).exists()

# Dashboard
@login_required
@user_passes_test(clinic_admin_required)
def clinic_admin_dashboard(request):
    clinic_admin = ClinicAdmin.objects.get(user=request.user)

    # Fetch all specialists (without filtering by clinic)
    specialists = Specialist.objects.all()

    # Fetch appointments linked to the clinic admin
    appointments = Appointment.objects.filter(user=clinic_admin.user)

    return render(
        request,
        "clinic_admins/clinic_admin_dashboard.html",
        {"specialists": specialists, "appointments": appointments},
    )

# Approve Specialist
@login_required
@user_passes_test(clinic_admin_required)
def approve_specialist(request, specialist_id):
    specialist = get_object_or_404(Specialist, id=specialist_id)
    specialist.is_active = True
    specialist.save()
    messages.success(request, f"✅ Specialist {specialist.user.first_name} has been approved!")
    return redirect("clinic_admin_dashboard")

# Suspend Specialist
@login_required
@user_passes_test(clinic_admin_required)
def suspend_specialist(request, specialist_id):
    specialist = get_object_or_404(Specialist, id=specialist_id)
    specialist.is_active = False
    specialist.save()
    messages.warning(request, f"⚠️ Specialist {specialist.user.first_name} has been suspended!")
    return redirect("clinic_admin_dashboard")


@login_required
@user_passes_test(clinic_admin_required)
def manage_appointments(request):
    clinic_admin = ClinicAdmin.objects.get(user=request.user)

    # Get all specialists linked to users
    specialists = Specialist.objects.all()  # Get all specialists

    # Filter appointments by specialists
    appointments = Appointment.objects.filter(specialist__in=specialists)

    return render(
        request,
        "clinic_admins/clinic_appointments.html",
        {"appointments": appointments}
    )



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ClinicAdminRegistrationForm
from .models import ClinicAdmin


def clinic_admin_register(request):
    if request.method == "POST":
        form = ClinicAdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration submitted! Wait for admin approval.")
            return redirect("clinic_admin_login")
    else:
        form = ClinicAdminRegistrationForm()

    return render(request, "clinic_admins/register.html", {"form": form})


def clinic_admin_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None and hasattr(user, "clinicadmin"):
            if user.clinicadmin.is_active:
                login(request, user)
                return redirect("clinic_admin_dashboard")
            else:
                messages.error(request, "Your account is awaiting admin approval.")
        else:
            messages.error(request, "Invalid credentials or not a clinic admin.")

    return render(request, "clinic_admins/login.html")


@login_required
@user_passes_test(clinic_admin_required)
def clinic_admin_dashboard(request):
    clinic_admin = ClinicAdmin.objects.get(user=request.user)

    # Fetch all specialists (without filtering by clinic)
    specialists = Specialist.objects.all()

    # Fetch appointments linked to the clinic admin
    appointments = Appointment.objects.filter(user=clinic_admin.user)

    return render(
        request,
        "clinic_admins/clinic_admin_dashboard.html",
        {
            "clinic_admin": clinic_admin,  # Add this line
            "specialists": specialists,
            "appointments": appointments
        },
    )


def clinic_admin_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("clinic_admin_login")

@login_required
@user_passes_test(clinic_admin_required)
def edit_clinic_details(request):
    clinic_admin = ClinicAdmin.objects.get(user=request.user)

    if request.method == "POST":
        clinic_admin.clinic_name = request.POST.get("clinic_name")
        clinic_admin.phone_number = request.POST.get("phone_number")
        clinic_admin.address = request.POST.get("address")
        clinic_admin.save()
        messages.success(request, "Clinic details updated successfully!")
        return redirect("clinic_admin_dashboard")

    return render(request, "clinic_admins/edit_clinic_details.html", {"clinic_admin": clinic_admin})


# Add Specialist
@login_required
@user_passes_test(clinic_admin_required)
def add_specialist(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        specialty = request.POST.get("specialty")
        credentials = request.POST.get("credentials")
        experience_years = request.POST.get("experience_years")
        bio = request.POST.get("bio")
        available_days = request.POST.get("available_days")
        working_hours = request.POST.get("working_hours")
        consultation_fee = request.POST.get("consultation_fee")
        accepts_virtual_consultations = request.POST.get("accepts_virtual_consultations") == "on"
        accepts_in_person_consultations = request.POST.get("accepts_in_person_consultations") == "on"

        # Create the User first
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = full_name
        user.save()

        # Create the Specialist profile
        specialist = Specialist.objects.create(
            user=user,
            full_name=full_name,
            specialty=specialty,
            credentials=credentials,
            experience_years=int(experience_years),
            bio=bio,
            available_days=available_days,
            working_hours=working_hours,
            consultation_fee=float(consultation_fee),
            accepts_virtual_consultations=accepts_virtual_consultations,
            accepts_in_person_consultations=accepts_in_person_consultations,
        )

        messages.success(request, f"Specialist {full_name} has been successfully added!")
        return redirect("clinic_admin_dashboard")

    return render(request, "clinic_admins/add_specialist.html")


@login_required
@user_passes_test(clinic_admin_required)
def assign_specialist(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    clinic_admin = ClinicAdmin.objects.get(user=request.user)

    # Get specialists from this clinic
    specialists = Specialist.objects.filter(clinic=clinic_admin)

    if request.method == "POST":
        specialist_id = request.POST.get("specialist_id")
        specialist = get_object_or_404(Specialist, id=specialist_id)
        appointment.specialist = specialist
        appointment.status = "confirmed"  # Mark appointment as assigned
        appointment.save()
        messages.success(request, f"Assigned {specialist.user.username} to appointment.")
        return redirect("manage_appointments")

    return render(
        request,
        "clinic_admins/assign_specialist.html",
        {"appointment": appointment, "specialists": specialists}
    )


