from django.urls import path
from . import views

urlpatterns = [
    path("submit/<int:treatment_id>/", views.submit_review, name="submit_review"),
    path("list/", views.reviews_list, name="review_list"),
]

