from django.urls import path
from . import views

urlpatterns = [
  
    path('', views.home, name='home' ),
    path('service/', views.service, name='service' ),
    path('blog/', views.blog, name='blog' ),
    path('blog_detail/<int:blog_id>/', views.blog_detail, name='blog_detail' ),
    path('tags/<int:category_id>/', views.tags, name='tags' ),
    
    
]
