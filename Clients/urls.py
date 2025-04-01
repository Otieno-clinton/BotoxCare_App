from django.urls import path
from . import views
from .views import update_profile

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    path("profile/update/", update_profile, name="update_profile"),
    path('', views.home, name='home'),



]

