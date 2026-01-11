from .models import Logo, SiteSetting, CompanyInformation  # Replace with your actual Logo model name
from .forms import BlogSearchForm, TestimonialForm, Contact, NewsLetterForm

def site_settings(request):
    return {
        'logo': Logo.objects.first(), # Grabs the first logo in your database
        'search_form': BlogSearchForm(request.GET or None), # This captures the query if it exists
        'testimonial_form': TestimonialForm(),
        'unread_messages': Contact.objects.filter(is_read=False).count(),
        'settings': SiteSetting.objects.first(),
        'address': CompanyInformation.objects.first(),
        'news_letter_form': NewsLetterForm()
    }