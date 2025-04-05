from django.shortcuts import render
from .models import Product, Category
from django.core.paginator import Paginator
from stores.models import Store  

def products(request):
    store_id = request.GET.get('store')
    category_id = request.GET.get('category')

    if store_id:
        products = Product.objects.filter(available=True, store_id=store_id).order_by('-created')
    else:
        products = Product.objects.filter(available=True).order_by('-created')

    if category_id:
        products = products.filter(categories__id=category_id)

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    stores = Store.objects.filter(active=True)

    return render(
        request,
        'products/products.html',
        {
            'products': page_obj,
            'categories': categories,
            'stores': stores,
            'selected_store': store_id,
        }
    )

def filter_products(request):
    store_id = request.GET.get('store')  
    category_id = request.GET.get('category') 

    if store_id and category_id:
        products = Product.objects.filter(
            available=True,
            store_id=store_id,
            categories__id=category_id
        ).order_by('-created')
    elif store_id:
        products = Product.objects.filter(
            available=True,
            store_id=store_id
        ).order_by('-created')
    elif category_id:
        products = Product.objects.filter(
            available=True,
            categories__id=category_id
        ).order_by('-created')
    else:
        products = Product.objects.filter(available=True).order_by('-created')

    # Paginación
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    stores = Store.objects.filter(active=True) 

    return render(
        request,
        'products/products.html',
        {
            'products': page_obj,
            'categories': categories,
            'stores': stores,
            'selected_store': store_id,  # La tienda actual
        }
    )