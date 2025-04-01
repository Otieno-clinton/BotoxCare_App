from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from appointments.models import Appointment
from specialists.models import Specialist
from treatments.models import Treatment


@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, "clients/appointments/appointment_list.html", {"appointments": appointments})


@login_required
def book_appointment(request):
    specialists = Specialist.objects.filter(is_verified=True)
    treatments = Treatment.objects.all()  # Fetch available treatments

    if request.method == "POST":
        specialist_id = request.POST.get("specialist")
        treatment_id = request.POST.get("treatment")  # Get treatment ID
        date = request.POST.get("date")

        if specialist_id and treatment_id and date:
            try:
                specialist = Specialist.objects.get(id=specialist_id)
                treatment = Treatment.objects.get(id=treatment_id)  # Get treatment object

                # Create appointment with both specialist and treatment
                appointment = Appointment.objects.create(
                    user=request.user, specialist=specialist, treatment=treatment, date=date
                )

                messages.success(request, "Appointment booked successfully! Please proceed to payment.")

                # Store appointment ID in session to track the latest booking
                request.session['last_appointment_id'] = appointment.id

                return redirect("appointment_list")  # Redirect to appointment list
            except (Specialist.DoesNotExist, Treatment.DoesNotExist):
                messages.error(request, "Invalid specialist or treatment selected.")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, "clients/appointments/book_appointment.html",
                  {"specialists": specialists, "treatments": treatments})


@login_required
def cancel_appointment(request, appointment_id):
    """Allows users to cancel an appointment."""
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if request.method == "POST":
        appointment.status = "Cancelled"
        appointment.save()
        messages.success(request, "Your appointment has been canceled successfully.")
        return redirect('appointment_list')

    return render(request, 'clients/appointments/cancel_appointment.html', {'appointment': appointment})
