from django.shortcuts import render, redirect
from django.urls import reverse
from beltechApp.models import *
from django.db.models import Count
from beltechApp.forms import BlogCommentForm, BlogSearchForm, TestimonialForm, ContactForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
def home(request):
    carousel = Carousel.objects.all()
    home_page_feature = Homepage_feature_area.objects.all()[:3]
    homepage_service = Homepage_service_area.objects.all()[:3]
    homepage_about = Homepage_about_area.objects.first()
    teams = Team.objects.all()

    latest_product = Already_done_project.objects.all().order_by('-date')[:2]
    recent_project_done = Products.objects.filter(is_latest =True)
    products = Products.objects.all()

    recent_blogs =BlogPost.objects.all().order_by('-created_at')[:3]

    testimony = Testimonial.objects.all()[:3]
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
        'logo': logo,
        'teams': teams,
        'paginators':testimony
        
    }
    return render(request, 'beltechApp/index.html', context)

def service(request):
    latest_product = Already_done_project.objects.all().order_by('-date')[:2]
    category = Category.objects.all()
    breadcrumb = printingHomePageImage.objects.all()
    products = Products.objects.all()

    features = Homepage_service_area.objects.all()[:3]

    recent_blogs =BlogPost.objects.all().order_by('-created_at')[:3]
    logo = Logo.objects.first()

    service =Service.objects.all()
    context = {
        'categories':category,
        'navs':breadcrumb,
        'products':products,
        'latests':latest_product,
        'recent_blogs':recent_blogs,
        'logo': logo,
        'features':features,
        'services':service
        
    }
    return render(request, 'beltechApp/service.html', context)

def blog(request):
    breadcrumb = printingHomePageImage.objects.all()
    blog = BlogPost.objects.all()
    products = Products.objects.all()

    paginator = Paginator(blog, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'paginators':page_obj,
        'navs':breadcrumb,
        'products':products,
    }
    return render(request, 'beltechApp/blog.html', context)

def blog_detail(request, blog_id):
    details = BlogPost.objects.get(id=blog_id)
    breadcrumb = printingHomePageImage.objects.all()

    blogpost =BlogPost.objects.all()
    recent_blog = blogpost.order_by('-created_at')[:3]

    category = Blog_category.objects.all()
    our_service_category = Category.objects.all()

    blog_comment = details.blopcomment.all()

    if request.method =='GET':
        search_form = BlogSearchForm(request.GET)
        if search_form.is_valid():
            search_string = search_form.cleaned_data.get('q')
            search_data = BlogPost.objects.filter(Q(title__icontains =search_string)| Q(slug__icontains =search_string)) if search_string else None
        else:
            search_form = BlogSearchForm()

    

    categories_with_counts = Category.objects.annotate(total_products=Count('services'))
    logo = Logo.objects.first()
    if request.method == 'POST':
        comment_form = BlogCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit =False)
            new_comment.blog = details
            new_comment.logo = logo

            # Check if this is a reply
            parent_id = request.POST.get('parent_id')
            if parent_id:
                new_comment.parent = BlogComment.objects.get(id=parent_id)

            new_comment.save()
            messages.info(request, 'Comment posted successfully!')
            # return('blog_detail', blog_id)
            return redirect(reverse('blog_detail', kwargs={'blog_id': blog_id}))
        else:
            messages.error(request, 'Check the data you input and try again!')
            return redirect(reverse('blog_detail', kwargs={'blog_id': blog_id}))
    else:
        comment_form = BlogCommentForm()

    context ={
        'blog':details,
        'navs':breadcrumb,
        'recent_blogs':recent_blog,
        'tags':category,
        'categorys':our_service_category,
        'product_count':categories_with_counts,
        'form': comment_form,
        'comments':blog_comment,
        'search_form':search_form,
        'search_data':search_data

        
    }
    return render(request, 'beltechApp/blog-details.html', context)

def tags(request, category_id):
    category =Blog_category.objects.get(id =category_id)
    blog_tags = BlogPost.objects.filter(category =category)

    breadcrumb = printingHomePageImage.objects.all()
    products = Products.objects.all()

    context ={
        'blogs':blog_tags,
        'navs':breadcrumb,
        'products':products,
        
        
    }
    return render(request, 'beltechApp/blog.html', context)

def service_tags(request, service_id):
    category =Category.objects.get(id =service_id)
    blog_tags = Products.objects.filter(category =category)

    breadcrumb = printingHomePageImage.objects.all()
    # products = Products.objects.all()

    latest_product = Already_done_project.objects.all().order_by('-date')[:2]
    category = Category.objects.all()
    recent_blogs =BlogPost.objects.all().order_by('-created_at')[:3]
    logo = Logo.objects.first()

    context ={
        'navs':breadcrumb,
        'categories':category,
        'products':blog_tags,
        'latests':latest_product,
        'recent_blogs':recent_blogs,
        'logo': logo
        
        
    }
    return render(request, 'beltechApp/service.html', context)


def search_results_view(request):
    product = Products.objects.all()
    query = request.GET.get('q')
   
    if query:
        # Search Products/Services
        product_results = Products.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()

    
    context ={
        'query': query,
        'products':product,
        'products': product_results,

    }
    return render(request, 'beltechApp/refactors/search_product.html', context)



def shop(request):
    all_products = Products.objects.all().order_by('-date')
    recent_product = all_products[:3]
    breadcrumb = printingHomePageImage.objects.all()
    category = Category.objects.all()

    # --- Pagination Logic ---
    # Show 6 products per page (change this number as you like)
    paginator = Paginator(all_products, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'paginators': page_obj,
        'navs': breadcrumb,
        'categorys': category,
        'recent_products': recent_product
    }

    return render(request, 'beltechApp/shop.html', context)

def about(request):
    about = Homepage_about_area.objects.first()
    # blog = BlogPost.objects.all()
    breadcrumb = printingHomePageImage.objects.all()
    faq = Faq.objects.all()[:3]
    team = Team.objects.all()[:3]

    process_video = ProcessVideo.objects.first()

    context = {
        'about': about,
        'blogs':blog,
        'navs': breadcrumb,
        'faqs':faq,
        'process_video': process_video,
        'teams':team
    }
    return render(request, 'beltechApp/about.html', context)

def testimonial(request):
    testimony = Testimonial.objects.all()
    breadcrumb = printingHomePageImage.objects.all()
    unapproved_count = Testimonial.objects.filter(is_approve=False).count()
    # testimony = Testimonial.objects.all()

    paginator = Paginator(testimony, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'paginators': page_obj,
        'navs': breadcrumb,
        'unapproved_count': unapproved_count
    }

    return render(request, 'beltechApp/testimonials.html', context)


def submit_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        
        if form.is_valid():
            # 1. Save the form but don't commit to DB yet
            testimony = form.save(commit=False)
            
            # 2. Assign the Logo (Grabbing the first one available)
            logo = Logo.objects.first() 
            testimony.logo_image = logo
            
            # 3. Force unapproved status for admin review
            testimony.is_approve = False
            
            # 4. Now save to database
            testimony.save()

            # If AJAX request, send JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'}, status=200)
            
            return redirect('testimonial')
        else:
            # If form is invalid (e.g. missing name), send errors
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
                
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def team(request):
    teams = Team.objects.all()
    breadcrumb = printingHomePageImage.objects.all()

    context = {
        'teams': teams,
        'navs':breadcrumb
    }
    return render(request, 'beltechApp/team.html', context)

def project(request):
    projects = Already_done_project.objects.all()
    breadcrumb = printingHomePageImage.objects.all()
    context = {
        'projects': projects,
        'navs':breadcrumb
    }
    return render(request, 'beltechApp/project.html', context)

def faq(request):
    breadcrumb = printingHomePageImage.objects.all()
    faqs = Faq.objects.all()[:3]
    context = {
        'faqs': faqs,
        'navs':breadcrumb
    }
    return render(request, 'beltechApp/faq.html', context)



def contact(request):
    breadcrumb = printingHomePageImage.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # This 'success' tag is what 'message.tags' looks for in HTML
            messages.success(request, 'Your message for Beltech Printing has been sent! We will call you shortly.')
            return redirect(reverse('contact') + '#contacts-form')
        else:
            messages.error(request, 'Please check your phone number or email format.')
    else:
        form = ContactForm()
    
    return render(request, 'beltechApp/contact.html', {'contact_form': form, 'navs':breadcrumb})