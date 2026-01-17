from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from beltechApp.models import *
from django.db.models import Count
from beltechApp.forms import BlogCommentForm, BlogSearchForm, TestimonialForm, ContactForm, NewsLetterForm,SendNewsletterForm

from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags



# Create your views here.
def home(request):
    carousel = Carousel.objects.all()
    home_page_feature = Homepage_feature_area.objects.all()[:3]
    homepage_service = Homepage_service_area.objects.all()[:3]
    homepage_about = Homepage_about_area.objects.first()
    teams = Team.objects.all()

    latest_product = Already_done_project.objects.all().order_by('-date')[:2]
    recent_project_done = Products.objects.filter(is_latest =True)
    # products = Products.objects.all()

    recent_blogs =BlogPost.objects.all().order_by('-created_at')[:3]

    testimony = Testimonial.objects.all()[:3]
    logo = Logo.objects.first()
    category = Category.objects.all()
    all_products = Products.objects.all().order_by('-date')[:3]
    context = {
        'carousels': carousel,
        'features': home_page_feature,
        'services': homepage_service,
        'about': homepage_about,
        'latests':latest_product,
        'recents': recent_project_done,
        # 'products':products,
        'blopaginators':recent_blogs,
        'logo': logo,
        'teams': teams,
        'paginators':testimony,
        'categories': category,
        'shoppaginators': all_products
        
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
        'blopaginators':recent_blogs,
        'logo': logo,
        'features':features,
        'services':service
        
    }
    return render(request, 'beltechApp/service.html', context)
def service_detail(request, service_id):
    products = Service.objects.get(id =service_id)

    context = {
        'product':products
    }
    return render(request, 'beltechApp/shop_detail.html', context)

def blog(request):
    breadcrumb = printingHomePageImage.objects.all()
    blog = BlogPost.objects.all()
    products = Products.objects.all()

    paginator = Paginator(blog, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    all_products = Products.objects.all().order_by('-date')[:3]

    context ={
        'blopaginators':page_obj,
        'navs':breadcrumb,
        'products':products,
        'shoppaginators': all_products
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
        'shoppaginators': page_obj,
        'navs': breadcrumb,
        'categorys': category,
        'recent_products': recent_product
    }

    return render(request, 'beltechApp/shop.html', context)

def shop_detail(request, shop_id):
    products = Products.objects.get(id =shop_id)

    context = {
        'product':products
    }
    return render(request, 'beltechApp/shop_detail.html', context)



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

def project_detail(request, proj_id):
    try:
        projectid = Already_done_project.objects.get(id =proj_id)
    except Already_done_project.DoesNotExist:
        messages.info(request, 'This project is no longer existing!')
    # product = Products.objects.first()
    context = {
        'project':projectid,
        # 'product':product
    }
    return render(request, 'beltechApp/shop_detail.html', context)
    

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
    address = CompanyInformation.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            save_message= form.save(commit =False)
            save_message.is_read =False
            save_message.save()
            # This 'success' tag is what 'message.tags' looks for in HTML
            messages.success(request, 'Your message for Beltech Printing has been sent! We will call you shortly.')
            return redirect(reverse('contact') + '#contacts-form')
        else:
            messages.error(request, 'Please check your phone number or email format.')
    else:
        form = ContactForm()
    context = {
        'contact_form': form, 
        'navs':breadcrumb,
        'address':address
    }
    return render(request, 'beltechApp/contact.html', context)




@login_required # Only the owner should see messages
def inbox(request):
    messages = Contact.objects.all().order_by('-date') # Newest first

    context = {
        'contact_messages': messages
        }
    return render(request, 'beltechApp/inbox.html', context)

def inbox_detail(request, pk):
    # Fetch the message or return 404 if not found
    msg = get_object_or_404(Contact, pk=pk)

    if msg.is_read == True:
        msg.is_read ==False
        msg.save()
    
    # Mark as read automatically when opened
    if not msg.is_read:
        msg.is_read = True
        msg.save()
        
    return render(request, 'beltechApp/inbox_detail.html', {'msg': msg})

def delete_message(request, pk):
    msg = get_object_or_404(Contact, pk=pk)
    msg.delete()
    messages.success(request, "Message deleted successfully.")
    return redirect('inbox')

def message_count(request):
    # Assuming you have a 'is_read' boolean field in your Contact model
    # If not, you can just count all: Contact.objects.count()
    count = Contact.objects.filter(is_read=False).count()
    return {'unread_messages': count}

def category_details(request, cat_id):
    category = Category.objects.get(id = cat_id)

    products = Products.objects.filter(category =category)

    context ={
        'category':category,
        'products':products
    }

    return render(request, 'beltechApp/category_detail.html', context)




def newsletter(request):
    if request.method == 'POST':
        news_letter_form = NewsLetterForm(request.POST)
        # Get the return URL once at the top
        return_url = request.META.get('HTTP_REFERER', '/')
        
        if news_letter_form.is_valid():
            # GET the email from the form data, not the database first()
            email = news_letter_form.cleaned_data.get('email')

            # Check if THIS specific email exists
            if NewsLetter.objects.filter(email=email).exists():
                messages.info(request, f'{email} is already a subscriber!')
            else:
                news_letter_form.save()
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            
            return redirect(return_url)
        else:
            messages.error(request, 'Please enter a valid email address.')
            return redirect(return_url)
            
    return redirect('/')


from django.core.mail import get_connection, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings

@user_passes_test(lambda u: u.is_staff) 
def send_newsletter_page(request):
    if request.method == 'POST':
        form = SendNewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message_body = form.cleaned_data['message']
            subscribers = NewsLetter.objects.all()
            
            if subscribers.exists():
                # Use our SITE_DOMAIN from settings.py
                domain = getattr(settings, 'SITE_DOMAIN', 'beltechprintingpress.onrender.com')
                
                # Open ONE connection for all emails (Huge speed boost!)
                connection = get_connection()
                email_messages = []

                for sub in subscribers:
                    context = {
                        'subject': subject,
                        'message': message_body,
                        'email': sub.email,
                        'domain': domain,
                        'unsubscribe_url': f"https://{domain}/newsletter/unsubscribe/{sub.email}/"
                    }
                    html_content = render_to_string('beltechApp/newsletter/news_letter_template.html', context)
                    text_content = strip_tags(html_content)

                    email = EmailMultiAlternatives(
                        subject, 
                        text_content, 
                        settings.DEFAULT_FROM_EMAIL, 
                        [sub.email],
                        connection=connection # Link to the shared connection
                    )
                    email.attach_alternative(html_content, "text/html")
                    email_messages.append(email)

                # Send all emails at once
                try:
                    connection.send_messages(email_messages)
                    messages.success(request, f"Successfully sent to {len(email_messages)} subscribers!")
                except Exception as e:
                    messages.error(request, f"SMTP Error: {e}")
                
                return redirect('send_newsletter_page')
    else:
        form = SendNewsletterForm()
    
    return render(request, 'beltechApp/newsletter/send_news.html', {'form': form})

# @user_passes_test(lambda u: u.is_staff) 
# def send_newsletter_page(request):
#     if request.method == 'POST':
#         form = SendNewsletterForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             message_body = form.cleaned_data['message']
#             subscribers = NewsLetter.objects.all()
            
#             if subscribers.exists():
#                 domain = request.get_host()
#                 for sub in subscribers:
#                     context = {
#                         'subject': subject,
#                         'message': message_body,
#                         'email': sub.email,
#                         'domain': domain,
#                         'unsubscribe_url': f"http://{domain}/newsletter/unsubscribe/{sub.email}/"
#                     }
#                     html_content = render_to_string('beltechApp/newsletter/news_letter_template.html', context)
#                     text_content = strip_tags(html_content)

#                     email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [sub.email])
#                     email.attach_alternative(html_content, "text/html")
                    
#                     try:
#                         email.send()
#                     except Exception as e:
#                         print(f"Error sending to {sub.email}: {e}")

#                 messages.success(request, f"Newsletter sent to {subscribers.count()} subscribers!")
#                 return redirect('send_newsletter_page')
#     else:
#         form = SendNewsletterForm()
    
#     return render(request, 'beltechApp/newsletter/send_news.html', {'form': form})


def unsubscribe(request, email):
    try:
        subscriber = NewsLetter.objects.get(email=email)
        subscriber.delete()
        messages.success(request, "You have been successfully unsubscribed.")
    except NewsLetter.DoesNotExist:
        messages.error(request, "Email not found in our list.")
    
    return redirect('home')
# @user_passes_test(lambda u: u.is_superuser) 
# def send_newsletter_page(request):
#     if request.method == 'POST':
#         form = SendNewsletterForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             message_text = form.cleaned_data['message']
            
#             # Get all subscriber objects (not just the email strings)
#             subscribers = NewsLetter.objects.all()
            
#             if subscribers.exists():
#                 success_count = 0
#                 error_occurred = False

#                 for sub in subscribers:
#                     # Data to send into the HTML file
#                     context = {
#                         'message': message_text,
#                         'email': sub.email,
#                         'domain': request.get_host() # Dynamically gets 127.0.0.1:8000 or your live site
#                     }
                    
#                     # Create the HTML and Plain Text versions
#                     html_content = render_to_string('beltechApp/newsletter/news_letter_template.html', context)
#                     text_content = strip_tags(html_content)

#                     # Setup the email
#                     email = EmailMultiAlternatives(
#                         subject=subject,
#                         body=text_content,
#                         from_email=settings.DEFAULT_FROM_EMAIL,
#                         to=[sub.email],
#                     )
#                     email.attach_alternative(html_content, "text/html")

#                     try:
#                         email.send()
#                         success_count += 1
#                     except Exception as e:
#                         print(f"Failed for {sub.email}: {e}")
#                         error_occurred = str(e)

#                 if success_count > 0:
#                     messages.success(request, f"Successfully sent to {success_count} subscribers.")
#                 if error_occurred:
#                     messages.error(request, f"Some emails failed. Last error: {error_occurred}")
            
#             return redirect('send_newsletter_page')
    
#     form = SendNewsletterForm()
#     return render(request, 'beltechApp/newsletter/send_news.html', {'form': form})

# @user_passes_test(lambda u: u.is_superuser) 
# def send_newsletter_page(request):
#     if request.method == 'POST':
#         form = SendNewsletterForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
            
#             subscribers = NewsLetter.objects.values_list('email', flat=True)
            
#             if subscribers:
#                 # --- START SAFETY NET ---
#                 try:
#                     send_mail(
#                         subject=subject,
#                         message=message,
#                         from_email = 'mathiaswilfred7@gmail.com', 
#                         recipient_list=list(subscribers),
#                         fail_silently=False,
#                     )
#                     messages.success(request, f"Newsletter sent successfully to {len(subscribers)} subscribers!")
#                 except Exception as e:
#                     # If it fails, we tell the admin WHY but don't crash the site
#                     print(f"SMTP Error: {e}")
#                     messages.error(request, f"Failed to send emails. Connection timed out. Error: {e}")
#                 # --- END SAFETY NET ---
#             else:
#                 messages.info(request, "You don't have any subscribers yet.")
                
#             return redirect('send_newsletter_page')
#     else:
#         form = SendNewsletterForm()
    
#     return render(request, 'beltechApp/newsletter/send_news.html', {'form': form})