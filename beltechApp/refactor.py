from django.db.models import Q
from .models import BlogPost, Product  # Import both models

def search_results_view(request):
    query = request.GET.get('q')
    blog_results = []
    product_results = []

    if query:
        # Search Blogs
        blog_results = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()

        # Search Products/Services
        product_results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()

    return render(request, 'search_results.html', {
        'query': query,
        'blog_results': blog_results,
        'product_results': product_results,
    })