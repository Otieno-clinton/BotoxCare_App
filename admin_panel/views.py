from django.shortcuts import render
from django.http import HttpResponse

def admin_dashboard(request):
    return HttpResponse("Admin Dashboard Page")

