from django import template
from django.db.models import QuerySet

from orders.models import Order

register = template.Library()


@register.simple_tag()
def get_orders(request) -> QuerySet:
    """
    Функция для отображения заказов на старице заказов
    """
    if request.user.is_authenticated:
        return Order.objects.filter(user=request.user).order_by('-created_timestamp')


@register.simple_tag()
def count_order(request):
    """
    Функция для получения количества заказов
    """
    count_order = 0
    orders = get_orders(request)
    if not  orders:
        return None

    for order in orders:
        if order.status == 'Отмена':
            pass
        else:
            count_order += 1
    return count_order
