from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Product
from goods.utils import filter_search, get_category_check, check


def corzina(request):
    return render(request, 'carts/corzina.html')


def detail_cart_add(request):
    product_id = request.POST.get("product_id")
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    else:
        carts = Cart.objects.filter(session_key=request.session.session_key, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)

    products_all = Product.objects.all()

    data = {
        'product': product,
        'products': products_all
    }

    cart_item_html = render_to_string(
        "goods/includes/include_detail_cart.html", data, request=request)

    response_data = {
        'message': "Товар добавлен в корзину",
        'cart_items_html': cart_item_html
    }
    return JsonResponse(response_data)


def cart_add(request):
    product_id = request.POST.get("product_id")
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    else:
        carts = Cart.objects.filter(session_key=request.session.session_key, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)

    data = {
        'product': product,
    }

    cart_item_html = render_to_string(
        "goods/includes/product-for-catalog.html", data, request=request)

    response_data = {
        'message': "Товар добавлен в корзину",
        'cart_items_html': cart_item_html
    }
    return JsonResponse(response_data)


def cart_remove(request):
    cart_id = request.POST.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()
    user_cart = get_user_carts(request)
    cart_item_html = render_to_string("carts/included/include_cart.html",
                                      {'carts': user_cart}, request=request)
    response_data = {
        'message': 'Товар удален',
        'cart_items_html': cart_item_html,
        'quantity_deleted': quantity,

    }
    return JsonResponse(response_data)


def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")
    cart = Cart.objects.get(id=cart_id)
    cart.quantity = quantity
    cart.save()

    cart = get_user_carts(request)
    cart_item_html = render_to_string("carts/included/include_cart.html",
                                      {'carts': cart}, request=request)
    response_data = {
        'cart_items_html': cart_item_html,
        'quantity': quantity,
    }
    return JsonResponse(response_data)


def cart_select(request):
    cart_id = request.GET.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    if cart.is_buy:
        cart.is_buy = False
        cart.save()
    else:
        cart.is_buy = True
        cart.save()
    cart = get_user_carts(request)
    cart_item_html = render_to_string("carts/included/include_cart.html",
                                      {'carts': cart}, request=request)
    response_data = {
        'cart_items_html': cart_item_html,
    }
    return JsonResponse(response_data)


def cart_select_all(request):
    check_all = request.GET.get("select_all")
    print(check_all)
    carts_id = request.GET.get("cart_id")
    carts = (carts_id.split('.'))
    for i in carts:
        cart = Cart.objects.get(id=int(i))
        if int(check_all) == 1:
            print(cart)
            cart.is_buy = True
            cart.save()
        else:
            cart.is_buy = False
            cart.save()

    cart = get_user_carts(request)
    cart_item_html = render_to_string("carts/included/include_cart.html",
                                      {'carts': cart, }, request=request)
    response_data = {
        'cart_items_html': cart_item_html,

    }
    return JsonResponse(response_data)


def cart_select_delete(request):
    if request.user.is_authenticated:
        query = Cart.objects.filter(user=request.user).filter(is_buy=True)
    else:
        query = Cart.objects.filter(session_key=request.session.session_key).filter(is_buy=True)
    for cart in query:
        cart.delete()
    return render(request, 'carts/corzina.html')
