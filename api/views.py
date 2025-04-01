from django.shortcuts import render
from django.http import JsonResponse

def api_treatments(request):
    data = {"message": "API - List of Treatments"}
    return JsonResponse(data)

def api_appointments(request):
    data = {"message": "API - List of Appointments"}
    return JsonResponse(data)
