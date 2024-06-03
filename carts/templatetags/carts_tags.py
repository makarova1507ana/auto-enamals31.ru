from django import template

from carts.models import Cart
from carts.utils import get_user_carts, get_user_carts_order
from goods.models import Product

register = template.Library()


def check_quantity(result):
    for i in result:
        if i.quantity >= i.product.quantity:
            quantity = i.product.quantity
            cart = Cart.objects.get(id=i.id)
            cart.quantity = quantity
            cart.save()
    return result


@register.simple_tag()
def user_carts(request):
    result = get_user_carts(request)
    return check_quantity(result)


@register.simple_tag()
def user_carts_order(request):
    result = get_user_carts_order(request)
    return check_quantity(result)


@register.simple_tag()
def user_carts_quantity(request):
    """
    Функция, которая проходится по запросу
    и создает список в котором не будет корзин в которой
    товаров = 0 и is_buy = false
    """
    list_product = []
    result = user_carts(request)
    for i in result:
        if i.quantity > 0:
            if i.is_buy:
                list_product.append(i)
    return list_product


@register.simple_tag()
def user_carts_for_catalog(request):
    count_ = []
    name_ = []
    result = get_user_carts(request)
    for res in result:
        count_.append(res.quantity)
        name_.append(res.product)
    the_dict = dict(zip(name_, count_))
    return the_dict


@register.simple_tag()
def check_select(request):
    result = get_user_carts(request)
    a = []
    for i in result:
        a.append(i.is_buy)
    print(a)
    if False in a:
        return False
    elif not a:
        return False
    else:
        return True


@register.simple_tag()
def is_delete(request):
    result = get_user_carts(request)
    a = []
    for i in result:
        a.append(i.is_buy)
    print(a)
    if True in a:
        return True
    elif not a:
        return False
    else:
        return False