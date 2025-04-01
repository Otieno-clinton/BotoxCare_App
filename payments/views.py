from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment
from .forms import PaymentForm  # Create this form
from payments.credentials import MpesaAccessToken, LipanaMpesaPpassword
import json

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests.auth import HTTPBasicAuth



@login_required
def payment_history(request):
    """View to display user's payment history."""
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'clients/payments/payment_history.html', {'payments': payments})


@login_required
def make_payment(request):
    """View to handle new payment creation."""
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            messages.success(request, "Payment successfully recorded!")
            return redirect('payment_history')  # Redirect to payment history page
    else:
        form = PaymentForm()

    return render(request, 'clients/payments/make_payment.html', {'form': form})


def token(request):
    consumer_key = '1ktP51i1jECFDDd8UdimELCE2cAZyjO4Uz6ufF5GDbpohIpd'
    consumer_secret = 'qUbtwAnveOESfoJ7M8sj0CbeQww6TmvpzMcoWiQm5iGwlKPGrF65MlZ65dmuZ5f1'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'clients/payments/pay.html')



def stk(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Clinton",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")

