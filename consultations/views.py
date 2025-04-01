from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

def consultation_list(request):
    return render(request, "clients/consultations/consultation_list.html")

def consultation_detail(request, id):
    return HttpResponse(f"Details of Consultation ID: {id}")

from django.shortcuts import render, get_object_or_404
from .models import Consultation

@login_required
def waiting_room(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    if request.user == consultation.specialist.user or request.user == consultation.user:
        return render(request, "clients/consultations/waiting_room.html", {"consultation": consultation})
    else:
        return redirect("home")  # Prevent unauthorized access


@login_required
def start_video_call(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    specialist = consultation.specialist

    if request.user != consultation.specialist.user:
        return redirect("home")  # Prevent unauthorized access

    return render(request, "clients/consultations/consultations.html", {"consultation": consultation})

def virtual_consultations(request):
    consultations = Consultation.objects.all()  # Fetch all consultations
    return render(request, "clients/consultations/consultations.html", {"consultations": consultations})

