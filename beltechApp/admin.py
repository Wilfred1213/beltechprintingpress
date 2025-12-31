from django.contrib import admin
from beltechApp.models import *
from django.utils.html import format_html

from django.utils.safestring import mark_safe

# Register your models here.

admin.site.register(Carousel)
admin.site.register(Homepage_feature_area)
admin.site.register(Homepage_service_area)
admin.site.register(Homepage_about_area)
admin.site.register(printingHomePageImage)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Display slug and description in the list view
    list_display = ('name', 'slug', 'image')
    # Automatically fill the slug field as you type the name
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    # def description_excerpt(self, obj):
    #     return obj.description[:50] + "..." if obj.description else ""
    # description_excerpt.short_description = "Description"


@admin.register(PrintingService)
class PrintingServiceAdmin(admin.ModelAdmin):
    # Show key details and a small image preview in the list
    list_display = ('display_image', 'name', 'category', 'base_price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'category__name')
    list_editable = ('base_price', 'is_available') # Edit prices directly from the list
    autocomplete_fields = ('category',) # Useful if you eventually have many categories

    # Method to display a small thumbnail in the admin list
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height:45px; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    
    display_image.short_description = 'Preview'

    # Organize the detail page into sections
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'category', 'is_available')
        }),
        ('Pricing & Media', {
            'fields': ('base_price', 'image'),
        }),
        ('Content', {
            'fields': ('description',),
        }),
    )


@admin.register(Already_done_project)
class AlreadyDoneProjectAdmin(admin.ModelAdmin):
    # Columns to show in the list view
    list_display = ('id', 'display_image', 'title', 'category', 'date')
    
    # Clickable links
    list_display_links = ('id', 'title')
    
    # Sidebar filters
    list_filter = ('category', 'date')
    
    # Search box
    search_fields = ('title', 'description')
    
    # Organizing the editor layout
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category')
        }),
        ('Content', {
            'fields': ('description',)
        }),
        ('Media', {
            'fields': ('image', 'image_preview'),
        }),
    )
    
    # Make image_preview read-only so it doesn't break the form
    readonly_fields = ('image_preview',)

    # Function to show a small thumbnail in the list
    def display_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="border-radius:5px;" />')
        return "No Image"
    display_image.short_description = 'Thumbnail'

    # Function to show a larger preview inside the edit page
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="300" style="border-radius:10px;" />')
        return "Upload an image to see preview"