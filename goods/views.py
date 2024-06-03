from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Categories, Subcategory
from .utils import get_category_check, q_search, filter_search, check, filter_search_sub


def categories(request):
    categories_all = Categories.objects.all()
    data = {
        'categories': categories_all,
    }
    return render(request, 'goods/cat_sub.html', data)


def subcategories(request, slug):
    category = Categories.objects.get(slug=slug)

    subcategory = Subcategory.objects.filter(category_id=category)
    data = {
        'categories': subcategory,
    }
    return render(request, 'goods/sub.html', data)


def catalog(request):
    page = request.GET.get('page', None)
    if page is None:
        page = 1

    products = filter_search(request)
    # Получение значений для фильтраций по категориям, брендам
    category_subcategory = get_category_check(products)
    category, subcategory, color, brands = category_subcategory[0], category_subcategory[1], category_subcategory[2], \
        category_subcategory[3]

    paginator = Paginator(products, 9)
    current_page = paginator.page(int(page))

    data = {
        'products': current_page,
        'category': check(category),
        'subcategory': check(subcategory),
        'color': check(color),
        'brands': check(brands),
    }

    return render(request, 'goods/catalog-2.html', data)


def catalog_sub(request, slug):
    page = request.GET.get('page', None)
    if page is None:
        page = 1

    products = filter_search_sub(request, slug)
    # Получение значений для фильтраций по категориям, брендам
    category_subcategory = get_category_check(products)
    category, subcategory, color, brands = category_subcategory[0], category_subcategory[1], category_subcategory[2], \
        category_subcategory[3]

    paginator = Paginator(products, 9)
    current_page = paginator.page(int(page))

    data = {
        'products': current_page,
        'category': check(category),
        'subcategory': check(subcategory),
        'color': check(color),
        'brands': check(brands)
    }

    return render(request, 'goods/catalog-2.html', data)


def get_detail_card_by_slug(request, slug):
    product = Product.objects.get(slug=slug)
    products_all = Product.objects.filter(subsubcategory=product.subsubcategory)
    data = {
        'product': product,
        # Количество товара которое отображается в похожих товарах
        'products': products_all[:3]
    }

    return render(request, 'goods/detail_cart.html', data)
