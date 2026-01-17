
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator, MaxValueValidator

from urllib.parse import urlparse, parse_qs
import urllib.parse



class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='customUser/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Account Management Staff'
    
    def __str__(self):
        return self.username

class Carousel(models.Model):
    discount = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='carousel/')
    # image2 = models.ImageField(upload_to='media/', null = True, blank=False)

    @property
    def imageUrl(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""
   
    def __str__(self):
        return self.title
    
class Homepage_feature_area(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='media/')
    def __str__(self):
        return self.title
class Homepage_service_area(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='service/')

    def __str__(self):
        return self.title
    
    @property
    def imageUrl(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""

class Homepage_about_area(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='about_image/', null=True)
    icon1 = models.CharField(max_length=100)
    description1 = models.CharField(max_length=500, null=True)
    icon2 = models.CharField(max_length=100)
    description2 = models.CharField(max_length=500, null=True)
    image1 = models.ImageField(upload_to='about_image/')
    image2 = models.ImageField(upload_to='about_image/')
    image3 = models.ImageField(upload_to='about_image/')
    image_expert= models.ImageField(upload_to='about_image/')
    phone = models.CharField(max_length=50)


    @property
    def imageUrl1(self):
        if self.image1 and hasattr(self.image1, 'url'):
            return self.image1.url
        return ""
    def imageUrl2(self):
        if self.image2 and hasattr(self.image2, 'url'):
            return self.image2.url
        return ""
    def imageUrl3(self):
        if self.image3 and hasattr(self.image3, 'url'):
            return self.image3.url
        return ""
    def imageUrl(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""

    def __str__(self):
        return self.title
    




# 1. CATEGORIES (e.g., Large Format, Corporate Stationery, Digital Print)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    # description = models.TextField(blank=True)
    image = models.ImageField(upload_to='services-category/', null =True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    def imageUrl(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""
    
class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default="Beltech Printing")
    whatsapp_number = models.CharField(
        max_length=15, 
        help_text="Enter number with country code, no plus sign (e.g., 2348030000000)"
    )
    business_address = models.TextField(default="Musty Global Plaza, Maiduguri")
    contact_email = models.EmailField(default="info@beltech.com.ng")

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # This ensures only one SiteSetting object exists
        if not self.pk and SiteSetting.objects.exists():
            return 
        return super(SiteSetting, self).save(*args, **kwargs)

# 2. PRINTING SERVICES (The specific products like "Business Cards")
class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    # Using CKEditor for rich descriptions (bullet points for specs, etc.)
    description = CKEditor5Field('Description', config_name='default')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit =models.CharField(max_length= 50, null=True, blank=True)
    image = models.ImageField(upload_to='services/')
    date = models.DateTimeField(auto_now_add=True, null=True)
    is_available = models.BooleanField(default=True)
    is_latest = models.BooleanField(default=False)

    def imageUrl(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""


    @property
    def whatsapp_link(self):
        # Pull the number from our Admin-controlled SiteSetting model
        config = SiteSetting.objects.first()
        phone = config.whatsapp_number if config else "2348000000000"
        
        message = f"Hello Beltech, I am interested in '{self.name}' (₦{self.base_price})."
        encoded_message = urllib.parse.quote(message)
        return f"https://wa.me/{phone}?text={encoded_message}"

    def __str__(self):
        return f"{self.name} - {self.category.name}"
    
class Service(models.Model):
    name = models.CharField(max_length=200)
    # Using CKEditor for rich descriptions (bullet points for specs, etc.)
    description = CKEditor5Field('Description', config_name='default')
    
    image = models.ImageField(upload_to='services/')
    date = models.DateTimeField(auto_now_add=True, null=True)
    

    def __str__(self):
        return f"{self.name}"
    
    def imageUrl(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""

class printingHomePageImage(models.Model):
    image = models.ImageField(upload_to='services/')

    class Meta:
        verbose_name = "Breadcrumb images"

    def imageUrl(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""

class Already_done_project(models.Model):
    title =models.CharField(max_length=50)
    description = CKEditor5Field('Description', config_name='default')
    image = models.ImageField(upload_to='projects/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='readymade')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"already done #{self.id} ({self.title})"
    
    def imageUrl(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""
    
class Logo(models.Model):
    name = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='logo/', help_text="Logo image")

    def __str__(self):
        return self.name
    
    def imageUrl(self):
        if self.main_image and hasattr(self.main_image, 'url'):
            return self.main_image.url
        return ""

class Blog_category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog category"
class BlogPost(models.Model):
    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Blog_category, on_delete=models.CASCADE, related_name='blopPost', null=True)
    
    # Images
    main_image = models.ImageField(upload_to='blog/main/', help_text="Featured image at the top")
    secondary_image = models.ImageField(upload_to='blog/secondary/', blank=True, null=True, help_text="Image for the middle of the article")
    
    # Content Areas
    content = CKEditor5Field('Body Content', config_name='default')
    
    # The Quote Area
    quote_text = models.TextField(blank=True, help_text="Special highlighted quote in the article")
    quote_author = models.CharField(max_length=100, blank=True, help_text="Author of the quote")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def imageUrl(self):
        if self.main_image and hasattr(self.main_image, 'url'):
            return self.main_image.url
        return ""

class BlogComment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='blopcomment', null=True)
    logo = models.ForeignKey(Logo, on_delete=models.CASCADE, related_name='logo', null=True)

    # reply
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Message from {self.name} - {self.email}"

    class Meta:
        ordering = ['-created_at']

class Faq(models.Model):
    question =models.CharField(max_length=200)
    answer = CKEditor5Field('Body Content', config_name='default')

    def __str__(self):
        return f"Question {self.question}"
    


class ProcessVideo(models.Model):
    title = models.CharField(
        max_length=200,
        default="How We Bring Your Ideas To Life"
    )
    sub_title = models.CharField(
        max_length=100,
        default="WATCH OUR PROCESS"
    )
    youtube_url = models.URLField(
        help_text="Paste a YouTube video URL (not playlist or channel)"
    )

    class Meta:
        verbose_name = "Process Video"
        verbose_name_plural = "Process Videos"

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        """
        Always return a VALID YouTube embed URL.
        Never return watch URLs.
        """
        parsed = urlparse(self.youtube_url)
        video_id = None

        # https://youtu.be/VIDEO_ID
        if parsed.netloc == "youtu.be":
            video_id = parsed.path.strip("/")

        # https://www.youtube.com/watch?v=VIDEO_ID
        elif "youtube.com" in parsed.netloc:
            qs = parse_qs(parsed.query)
            video_id = qs.get("v", [None])[0]

            # https://www.youtube.com/embed/VIDEO_ID
            if not video_id and "embed" in parsed.path:
                video_id = parsed.path.split("/")[-1]

        if not video_id:
            return ""

        return f"https://www.youtube.com/embed/{video_id}"

class Team(models.Model):
     name = models.CharField(max_length=200)
     image = models.ImageField(upload_to='services/')
     role = models.CharField(max_length=200)

     def __str__(self):
         return self.name
     
     def imageUrl(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""
     
class Testimonial(models.Model):
    name = models.CharField(max_length=100, help_text="Client or customer name")
    message = models.TextField(help_text="Client testimonial message")
    logo_image = models.ForeignKey(Logo, on_delete=models.CASCADE, null=True)
    # rating = models.PositiveSmallIntegerField(default=5, help_text="Rating from 1 to 5")
    rating = models.IntegerField(
        default=5, 
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True,
        help_text="Rate from 1 to 5"
    )
    main_image = models.ImageField(upload_to='blog/main/', null=True, blank=True, help_text="Featured image at the top")
    is_active = models.BooleanField(default=True, help_text="Show or hide this testimonial on the site")
    is_approve = models.BooleanField(default=True, help_text="Admin approve or decline the testimony")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.rating}★)"
    
    def logImageUrl(self):
        if self.logo_image and hasattr(self.logo_image, 'url'):
            return self.logo_image.url
        return ""
    def mainImageUrl(self):
        if self.main_image and hasattr(self.main_image, 'url'):
            return self.main_image.url
        return ""
    

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, help_text="User's email address")
    phone_number = models.CharField(max_length=20, null=True, help_text="e.g. +234 800 000 0000")
    message = CKEditor5Field('Description', config_name='default')
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=True, help_text="This indicate that you have read this message")


    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-date']

    def __str__(self):
        return f"Message from {self.full_name} - {self.email}"

class CompanyInformation(models.Model):
    name = models.CharField(max_length=100, default="Beltech Printing")
    address = models.CharField(max_length=255, help_text="e.g. Shop No. A 6, Musty Global Plaza")
    street = models.CharField(max_length=255, help_text="e.g. Circular Road")
    landmark = models.CharField(max_length=255, help_text="e.g. Opposite Nanne and Boi")
    city_state = models.CharField(max_length=100, default="Maiduguri, Borno State")
    about = models.CharField(max_length=200, default='Beltech Printing & ICT Hub (commonly referred to as Beltech Printing Press) is a multi-service business that bridges the gap between traditional high-quality printing and modern digital technology.')
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    
    # This stores the Google Maps Embed URL
    google_maps_link = models.TextField(help_text="Paste the iframe 'src' link here")

    class Meta:
        verbose_name_plural = "Company Information"

    def __str__(self):
        return self.name
    
class NewsLetter(models.Model):
    email = models.EmailField(max_length=254)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email