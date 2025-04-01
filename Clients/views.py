from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth import logout

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm


# ---------------- Authentication ----------------

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "clients/auth/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # ✅ Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect("register")

        # ✅ Create user with first_name, last_name, and email
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )

        # ✅ Create Profile for the user
        profile = Profile.objects.create(user=user, email=email)

        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect("login")  # Redirect to profile page

    return render(request, "clients/auth/register.html")





@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "clients/auth/profile.html", {"profile": profile})


@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Redirect to profile page after updating
    else:
        form = ProfileForm(instance=profile)

    return render(request, "clients/auth/update_profile.html", {"form": form})



















# ---------------- Consultations ----------------

@login_required
def consultation_list_view(request):
    consultations = Consultation.objects.filter(user=request.user)
    return render(request, "clients/consultations/consultation_list.html", {"consultations": consultations})


@login_required
def consultation_detail_view(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id, user=request.user)
    return render(request, "clients/consultations/consultation_detail.html", {"consultation": consultation})


# ---------------- Payments ----------------

@login_required
def payment_history_view(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, "clients/payments/payment_history.html", {"payments": payments})


@login_required
def make_payment_view(request):
    if request.method == "POST":
        amount = request.POST["amount"]
        Payment.objects.create(user=request.user, amount=amount)
        messages.success(request, "Payment successful!")
        return redirect("payment_history")

    return render(request, "clients/payments/make_payment.html")








def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page or another appropriate page

def home(request):
    return render(request, "home.html")

def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile, created = Profile.objects.get_or_create(user=user)
            if not profile.phone or not profile.address:  # Check if profile is incomplete
                return redirect("update_profile")  # Redirect to update profile
            return redirect("profile")  # Redirect to profile if complete
    return render(request, "clients/auth/login.html")

