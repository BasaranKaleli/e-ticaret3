from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from page.views import STATUS

def category_show(request, category_slug):
    context = dict()
    context['category'] = get_object_or_404(Category, slug=category_slug)
    
    context['items'] = Product.objects.filter(
        category=context['category'],
        status=STATUS,
        stock__gte=1,
    )

    
    page = request.GET.get('page', 1)
    paginator = Paginator(context['items'], 10) 
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context['items'] = items

    
    sort_by = request.GET.get('sort', 'default') 
    if sort_by == 'price_low':
        context['items'] = context['items'].order_by('price')
    elif sort_by == 'price_high':
        context['items'] = context['items'].order_by('-price')
    elif sort_by == 'name':
        context['items'] = context['items'].order_by('title')

    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        context['items'] = context['items'].filter(price__range=(min_price, max_price))

    return render(request, 'product/category_show.html', context)
