from django.shortcuts import render
from beltechApp.models import *

# Create your views here.
def home(request):
    carousel = Carousel.objects.all()
    home_page_feature = Homepage_feature_area.objects.all()[:3]
    homepage_service = Homepage_service_area.objects.all()[:3]
    homepage_about = Homepage_about_area.objects.first()

    latest_product = Already_done_project.objects.all().order_by('-date')[:2]
    context = {
        'carousels': carousel,
        'features': home_page_feature,
        'services': homepage_service,
        'about': homepage_about,
        'latests':latest_product,
    }
    return render(request, 'beltechApp/index.html', context)

def service(request):
    category = Category.objects.all()
    homepagenav = printingHomePageImage.objects.all()
    products = PrintingService.objects.all()
    context = {
        'categories':category,
        'navs':homepagenav,
        'products':products
        
    }
    return render(request, 'beltechApp/service.html', context)