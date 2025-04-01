from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from reviews.models import Review


from django.shortcuts import render
from .models import Review
from treatments.models import Treatment

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from treatments.models import Treatment

def reviews_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    treatments = Treatment.objects.all()  # Fetch available treatments
    return render(request, "clients/reviews/review_list.html", {"reviews": reviews, "treatments": treatments})


@login_required
def submit_review(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    treatments = Treatment.objects.all()  # Get all treatments

    if request.method == "POST":
        rating = request.POST["rating"]
        content = request.POST["review"]

        # Create and save review
        Review.objects.create(
            user=request.user,
            treatment=treatment,  # Associate the review with the treatment
            rating=rating,
            content=content
        )
        messages.success(request, "Review submitted successfully!")
        return redirect("review_list")


    return render(request, "clients/reviews/submit_review.html", {
        "treatments": treatments,
        "selected_treatment_id": treatment_id  # Pass the ID to match the template
    })