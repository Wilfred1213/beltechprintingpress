from .models import Logo  # Replace with your actual Logo model name
from .forms import BlogSearchForm

def site_settings(request):
    return {
        'logo': Logo.objects.first(), # Grabs the first logo in your database
        'search_form': BlogSearchForm(request.GET or None) # This captures the query if it exists
    }