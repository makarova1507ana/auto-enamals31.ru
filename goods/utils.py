from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q

from goods.models import Product


def get_category_check(data_query_set):
    """
    Функция для создания категорий поиска
    :param data_query_set:
    :return:
    """
    category = []
    subcategory = []
    color = []
    brand = []
    for i in data_query_set:
        if i.brand not in brand:
            brand.append(i.brand)
        if i.category not in category:
            category.append(i.category)
        if i.subcategory not in subcategory:
            subcategory.append(i.subcategory)
        if i.color not in color:
            color.append(i.color)
    return category, subcategory, color, brand


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Product.objects.filter(id=int(query))

    vector = SearchVector("description", "name")
    query = SearchQuery(query)

    return Product.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by('-rank')


def filter_search(request):
    """
    Функция для получения get параметров и фильтрация
    :param request:
    :return:
    """

    query = request.GET.get('q', None)
    order_by = request.GET.get('order_by', None)
    on_sale = request.GET.get('on_sale', None)
    subcategory = request.GET.get('subcategory', None)
    category = request.GET.get('category', None)
    brand = request.GET.get('brand', None)
    is_stock = request.GET.get('is_stock', None)
    color = request.GET.get('color', None)
    print(color)
    print(query)
    if query:
        products = q_search(query)
    else:
        products = Product.objects.all()
    if on_sale:
        products = products.filter(discount__gt=0)
    if order_by == 'price':
        products = products.order_by('price')
    if order_by == '-price':
        products = products.order_by('-price')
        print(products)
        for i in products:
            print(i.sell_price())
    if color:
        products = products.filter(color__name=color)
    if subcategory:
        products = products.filter(subcategory__name=subcategory)
    if category:
        products = products.filter(category__name=category)
    if brand:
        products = products.filter(brand__name=brand)
    if is_stock:
        products = products.filter(quantity__gt=0)

    return products


def filter_search_sub(request, slug):
    """
    Функция для получения get параметров и фильтрация
    :param request:
    :return:
    """
    query = request.GET.get('q', None)
    order_by = request.GET.get('order_by', None)
    on_sale = request.GET.get('on_sale', None)
    subcategory = request.GET.get('subcategory', None)
    category = request.GET.get('category', None)
    brand = request.GET.get('brand', None)
    is_stock = request.GET.get('is_stock', None)

    if query:
        products = q_search(query)
    else:
        products = Product.objects.filter(subcategory__slug=slug)
    if on_sale:
        products = products.filter(discount__gt=0)
    if order_by == 'price':
        products = products.order_by('price')
    if order_by == '-price':
        products = products.order_by('-price')
        print(products)
        for i in products:
            print(i.sell_price())
    if subcategory:
        products = products.filter(subcategory__name=subcategory)
    if category:
        products = products.filter(category__name=category)
    if brand:
        products = products.filter(brand__name=brand)
    if is_stock:
        products = products.filter(quantity__gt=0)

    return products


def check(list_data):
    if len(list_data) == 1:
        if list_data[0] is None:
            return None
        else:
            return list_data
    else:
        return list_data
