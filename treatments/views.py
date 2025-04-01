from django.shortcuts import render, get_object_or_404

from treatments.models import Treatment


def treatment_list(request):
    treatments = Treatment.objects.all()
    return render(request, "clients/treatments/treatment_list.html", {"treatments": treatments})

def treatment_detail(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    return render(request, "clients/treatments/treatment_detail.html", {"treatment": treatment})
