from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Contact  # Replace with your actual model name

# signals.py
from django.core.mail import send_mail
from .models import NewsLetter

@receiver(post_save, sender=Contact)
def send_contact_email_notification(sender, instance, created, **kwargs):
    if created:  # Only send email when a new record is created
        context = {
            'name': instance.full_name,
            'email': instance.email,
            'phone': instance.phone_number,
            'message': instance.message,
        }
        
        # Render HTML template
        html_content = render_to_string('beltechApp/emails/contact_notification.html', context)
        text_content = strip_tags(html_content)

        subject = f"New Lead from Beltech: {instance.full_name}"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [settings.EMAIL_HOST_USER] # Sends to your Gmail

        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")

        try:
            email.send()
        except Exception as e:
            print(f"Signal Email Error: {e}")



@receiver(post_save, sender=NewsLetter)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Beltech Printing!"
        domain = "127.0.0.1:8000" # Update this to your real domain later
        
        context = {
            'subject': subject,
            'message': "Thanks for joining us! We'll keep you updated with our latest deals and printing tips.",
            'email': instance.email,
            'domain': domain,
            'unsubscribe_url': f"http://{domain}/newsletter/unsubscribe/{instance.email}/"
        }

        html_content = render_to_string('beltechApp/newsletter/news_letter_template.html', context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [instance.email])
        email.attach_alternative(html_content, "text/html")

        try:
            email.send()
        except Exception as e:
            print(f"Welcome signal failed: {e}")
# @receiver(post_save, sender=NewsLetter)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created:
#         subject = "Welcome to Beltech Printing!"
#         message = f"Hi {instance.email},\n\nThank you for subscribing to our newsletter. We will keep you updated on our latest printing deals!"
#         from_email = 'mathiaswilfred7@gmail.com'
#         # ... your subject/message code ...
#         try:
#             send_mail(subject, message, from_email, [instance.email])
#         except Exception as e:
#             print(f"Welcome Email Failed: {e}") # This prevents the crash