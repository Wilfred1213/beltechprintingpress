
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    # Ensure the class name is exactly 'CustomUser'
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username

class Carousel(models.Model):
    discount = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')
    image2 = models.ImageField(upload_to='media/', null = True, blank=False)


    def __str__(self):
        return self.title
    
class Homepage_feature_area(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='media/')
class Homepage_service_area(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')

class Homepage_about_area(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/', null=True)
    icon1 = models.CharField(max_length=100)
    description1 = models.CharField(max_length=200, null=True)
    icon2 = models.CharField(max_length=100)
    description2 = models.CharField(max_length=200, null=True)
    image1 = models.ImageField(upload_to='media/')
    image2 = models.ImageField(upload_to='media/')
    image3 = models.ImageField(upload_to='media/')
    image_expert= models.ImageField(upload_to='media/')
    phone = models.CharField(max_length=50)

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

# 2. PRINTING SERVICES (The specific products like "Business Cards")
class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    # Using CKEditor for rich descriptions (bullet points for specs, etc.)
    description = CKEditor5Field('Description', config_name='default')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/')
    date = models.DateTimeField(auto_now_add=True, null=True)
    is_available = models.BooleanField(default=True)
    is_latest = models.BooleanField(default=False)

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

class printingHomePageImage(models.Model):
    image = models.ImageField(upload_to='services/')
    

# 3. ORDERS (Tracking customer uploads and status)
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('printing', 'Printing in Progress'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed/Delivered'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Products, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    
    # Critical for Beltech: The print-ready file
    design_file = models.FileField(upload_to='orders/%Y/%m/%d/')
    special_instructions = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Business Logic: Auto-calculate the price
        self.total_cost = self.service.base_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} ({self.service.name})"
    

class Already_done_project(models.Model):
    title =models.CharField(max_length=50)
    description = CKEditor5Field('Description', config_name='default')
    image = models.ImageField(upload_to='projects/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='readymade')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"already done #{self.id} ({self.title})"
    
class Logo(models.Model):
    name = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='logo/', help_text="Logo image")

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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    
from django.db import models

from django.db import models
from urllib.parse import urlparse, parse_qs


from django.db import models
from urllib.parse import urlparse, parse_qs


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
     
from django.db import models


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
    

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, help_text="User's email address")
    phone_number = models.CharField(max_length=20, null=True, help_text="e.g. +234 800 000 0000")
    message = CKEditor5Field('Description', config_name='default')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-date']

    def __str__(self):
        return f"Message from {self.full_name} - {self.email}"

    
