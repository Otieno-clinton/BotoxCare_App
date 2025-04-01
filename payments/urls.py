from django.urls import path
from . import views

urlpatterns = [
    path('pyment_history', views.payment_history, name='payment_history'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),
]
