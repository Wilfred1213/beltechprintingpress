from django.urls import path
from . import views

urlpatterns = [
  
    path('', views.home, name='home' ),
    path('service/', views.service, name='service' ),
    path('blog/', views.blog, name='blog' ),
    path('blog_detail/<int:blog_id>/', views.blog_detail, name='blog_detail' ),
    path('tags/<int:category_id>/', views.tags, name='tags' ),
    path('service_tags/<int:service_id>/', views.service_tags, name='service_tags' ),
    path('search_results_view/', views.search_results_view, name='search_results_view' ),
    path('shop/', views.shop, name='shop' ),
    path('about/', views.about, name='about' ),
    path('testimonial/', views.testimonial, name='testimonial' ),
    path('submit_testimonial/', views.submit_testimonial, name='submit_testimonial' ),
    path('team/', views.team, name='team' ),
    path('project/', views.project, name='project' ),
    path('faq/', views.faq, name='faq' ),
    path('contact/', views.contact, name='contact' ),
    path('inbox/', views.inbox, name='inbox' ),
    path('inbox_detail/<int:pk>/', views.inbox_detail, name='inbox_detail'),
    path('message_count/', views.message_count, name='message_count' ),
    path('delete_message/<int:pk>/delete/', views.delete_message, name='delete_message'),
    path('category_details/<int:cat_id>/delete/', views.category_details, name='category_details')
    
]
