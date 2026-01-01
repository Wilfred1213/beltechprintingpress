from django.shortcuts import render
from beltechApp.models import *

# Create your views here.
def home(request):
    carousel = Carousel.objects.all()
    home_page_feature = Homepage_feature_area.objects.all()[:3]
    homepage_service = Homepage_service_area.objects.all()[:3]
    homepage_about = Homepage_about_area.objects.first()

    latest_product = Already_done_project.objects.all().order_by('-date')[:2]
    recent_project_done = PrintingService.objects.filter(is_latest =True)
    products = PrintingService.objects.all()

    recent_blogs =BlogPost.objects.all().order_by('-created_at')[:3]
    logo = Logo.objects.first()
    context = {
        'carousels': carousel,
        'features': home_page_feature,
        'services': homepage_service,
        'about': homepage_about,
        'latests':latest_product,
        'recents': recent_project_done,
        'products':products,
        'recent_blogs':recent_blogs,
        'logo': logo
        
    }
    return render(request, 'beltechApp/index.html', context)

def service(request):
    latest_product = Already_done_project.objects.all().order_by('-date')[:2]
    category = Category.objects.all()
    breadcrumb = printingHomePageImage.objects.all()
    products = PrintingService.objects.all()

    recent_blogs =BlogPost.objects.all().order_by('-created_at')[:3]
    logo = Logo.objects.first()
    context = {
        'categories':category,
        'navs':breadcrumb,
        'products':products,
        'latests':latest_product,
        'recent_blogs':recent_blogs,
        'logo': logo
        
    }
    return render(request, 'beltechApp/service.html', context)

def blog(request):
    breadcrumb = printingHomePageImage.objects.all()
    blog = BlogPost.objects.all()
    products = PrintingService.objects.all()

    context ={
        'blogs':blog,
        'navs':breadcrumb,
        'products':products,
    }
    return render(request, 'beltechApp/blog.html', context)

def blog_detail(request, blog_id):
    details = BlogPost.objects.get(id=blog_id)
    breadcrumb = printingHomePageImage.objects.all()
    recent_blog = BlogPost.objects.all().order_by('-created_at')[:3]

    category = Blog_category.objects.all()

    context ={
        'blog':details,
        'navs':breadcrumb,
        'recent_blogs':recent_blog,
        'tags':category

        
    }
    return render(request, 'beltechApp/blog-details.html', context)

def tags(request, category_id):
    category =Blog_category.objects.get(id =category_id)
    blog_tags = BlogPost.objects.filter(category =category)

    breadcrumb = printingHomePageImage.objects.all()
    products = PrintingService.objects.all()

    context ={
        'blogs':blog_tags,
        'navs':breadcrumb,
        'products':products,
        
        
    }
    return render(request, 'beltechApp/blog.html', context)


