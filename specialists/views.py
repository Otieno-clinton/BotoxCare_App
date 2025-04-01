from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Specialist
from appointments.models import Appointment
from reviews.models import Review
from payments.models import Payment
from consultations.models import Consultation


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Specialist

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Specialist


def specialist_register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        specialty = request.POST['specialty']
        credentials = request.POST['credentials']
        experience_years = int(request.POST.get('experience_years', 0))
        bio = request.POST.get('bio', '')
        available_days = request.POST['available_days']
        working_hours = request.POST['working_hours']
        consultation_fee = float(request.POST.get('consultation_fee', 0.00))
        accepts_virtual_consultations = 'accepts_virtual_consultations' in request.POST
        accepts_in_person_consultations = 'accepts_in_person_consultations' in request.POST

        # ✅ Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another one.")
            return redirect('specialist_register')

        # ✅ Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Please use another email.")
            return redirect('specialist_register')

        # ✅ Create user account
        user = User.objects.create_user(username=username, email=email, password=password)

        # ✅ Create specialist profile
        specialist = Specialist.objects.create(
            user=user,
            full_name=full_name,
            specialty=specialty,
            credentials=credentials,
            experience_years=experience_years,
            bio=bio,
            available_days=available_days,
            working_hours=working_hours,
            consultation_fee=consultation_fee,
            accepts_virtual_consultations=accepts_virtual_consultations,
            accepts_in_person_consultations=accepts_in_person_consultations,
        )

        # ✅ Log the specialist in
        login(request, user)

        messages.success(request, "Registration successful! Please update your profile.")

        # ✅ Redirect to the specialist's profile update page
        return redirect('specialist_profile', specialist_id=specialist.id)

    return render(request, 'specialists/auth/register.html')


@login_required
def dashboard(request):
    specialist = get_object_or_404(Specialist, user=request.user)
    total_consultations = Consultation.objects.filter(specialist=specialist).count()
    upcoming_appointments = Appointment.objects.filter(specialist=specialist, status="Scheduled")

    context = {
        'specialist': specialist,
        'total_consultations': total_consultations,
        'upcoming_appointments_count': upcoming_appointments.count(),
    }
    return render(request, 'specialists/dashboard.html', context)

def specialist_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_specialist:  # ✅ No more AttributeError
                login(request, user)
                return redirect('specialist_dashboard')  # Redirect to the specialist's dashboard
            else:
                messages.error(request, 'You are not registered as a specialist.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'specialists/auth/login.html')




from django.shortcuts import get_object_or_404

def specialist_profile(request, specialist_id):
    specialist = get_object_or_404(Specialist, id=specialist_id)

    if request.method == 'POST':
        specialist.full_name = request.POST['full_name']
        specialist.specialty = request.POST['specialty']
        specialist.credentials = request.POST['credentials']
        specialist.experience_years = request.POST['experience_years']
        specialist.bio = request.POST['bio']
        specialist.available_days = request.POST['available_days']
        specialist.working_hours = request.POST['working_hours']
        specialist.consultation_fee = request.POST['consultation_fee']
        specialist.accepts_virtual_consultations = 'accepts_virtual_consultations' in request.POST
        specialist.accepts_in_person_consultations = 'accepts_in_person_consultations' in request.POST
        specialist.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('specialist_dashboard')  # Redirect to the specialist dashboard after updating

    return render(request, 'specialists/auth/profile.html', {'specialist': specialist})



@login_required
def manage_appointments(request):
    specialist = get_object_or_404(Specialist, user=request.user)
    appointments = Appointment.objects.filter(specialist=specialist)
    return render(request, 'specialists/appointments_management.html', {'appointments': appointments})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from appointments.models import Appointment

def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "Scheduled"
    appointment.save()
    messages.success(request, "Appointment approved successfully!")
    return redirect("specialist_appointments")  # Ensure this redirect URL exists in urls.py

def decline_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "Cancelled"
    appointment.save()
    messages.success(request, "Appointment declined.")
    return redirect("specialist_appointments")


@login_required
def consultations(request):
    specialist = get_object_or_404(Specialist, user=request.user)
    consultations = Consultation.objects.filter(specialist=specialist)
    return render(request, 'specialists/consultations.html', {'consultations': consultations})


@login_required
def reviews(request):
    specialist = get_object_or_404(Specialist, user=request.user)
    reviews = Review.objects.filter(treatment__appointment__specialist=specialist)
    return render(request, 'specialists/specialist_reviews.html', {'reviews': reviews})


# @login_required
# def reviews(request):
#     user = request.user
#
#     # Fetch reviews only for treatments provided by the logged-in specialist
#     reviews = Review.objects.filter(treatment__specialist=user).order_by("-created_at")
#
#     return render(request, "specialists/specialist_reviews.html", {"reviews": reviews})

@login_required
def payments(request):
    specialist = get_object_or_404(Specialist, user=request.user)
    payments = Payment.objects.filter(user=specialist.user)
    return render(request, 'specialists/payments.html', {'payments': payments})


# @login_required
# def support(request):
#     return render(request, 'specialists/support.html')

@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()  # Fetch all appointments
    return render(request, 'specialists/confirmation.html', {'appointments': appointments})

