from django.core.mail import send_mail
from django.conf import settings


def send_appointment_confirmation(user, specialist, treatment, date):
    subject = "Appointment Confirmation"
    message = f"Dear {user.username},\n\n"
    message += f"Your appointment with {specialist.full_name} ({specialist.specialty}) "
    message += f"for {treatment.name} on {date} has been confirmed.\n\n"
    message += "Thank you for choosing our service.\n\nBest Regards."

    recipient_email = "user.email"  # Ensure this is not empty!

    if recipient_email:  # ✅ Only send if email exists
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])
        print(f"✅ Email successfully sent to {recipient_email}")
    else:
        print("❌ Email not sent: No recipient email found!")
