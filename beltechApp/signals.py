from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Contact  # Replace with your actual model name

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