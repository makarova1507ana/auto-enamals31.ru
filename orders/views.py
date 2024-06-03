from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from carts.models import Cart
from goods.models import Product
from orders.forms import CreateOrderForm
from orders.models import OrderItem, Order
from orders.utils import send_email_order
from users.forms import UserRegistrationForm


# Create your views here.
@login_required
def order_(request):
    form = UserRegistrationForm(instance=request.user)
    context = {
        'title': 'Кабинет',
        'form': form,
    }
    return render(request, 'orders/order.html', context)


@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user).filter(quantity__gt=0).filter(is_buy=True)

                    if cart_items.exists():
                        # Создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        # Создать заказанные товары
                        for cart_item in cart_items:
                            if cart_item.quantity <= 0:
                                pass
                            elif not cart_item.is_buy:
                                pass
                            else:
                                product = cart_item.product
                                name = cart_item.product.name
                                price = cart_item.product.sell_price()
                                quantity = cart_item.quantity

                                if product.quantity < quantity:
                                    raise ValidationError(f'Недостаточное количество товара {name} на складе\
                                                           В наличии - {product.quantity}')

                                OrderItem.objects.create(
                                    order=order,
                                    product=product,
                                    name=name,
                                    price=price,
                                    quantity=quantity,
                                )
                                product.quantity -= quantity
                                product.save()

                        # Очистить корзину пользователя после создания заказа
                        cart_items.delete()
                        id_order = order.id

                        # Отправка сообщения на почту
                        send_email_order(
                            request,
                            user,
                            order,
                            'orders/notification_email/paid_processed.html',
                            'Заказ оплачен и находится в обработке '
                        )

                        messages.success(request, 'Заказ оформлен!')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('cart:order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'orders': True,
    }
    return render(request, 'orders/create_order.html', context=context)


def orderlist(request, id_user):
    user = request.user
    if user.id == id_user:
        return render(request, 'orders/orders_show.html')
    else:
        return render(request, '404.html')


def get_detail_order_by_id(request, id_order, id_user):
    user = request.user
    if user.id != id_user:
        return render(request, '404.html')
    products_all = OrderItem.objects.filter(order=id_order)

    print(products_all)
    order = Order.objects.get(id=id_order)
    print(order.status)
    is_cancel = order.status == 'В обработке'
    print(is_cancel)
    data = {
        'OrderItems': products_all,
        'id_order': id_order,
        'is_cancel': is_cancel,
    }

    return render(request, 'orders/detail_order.html', data)


def cancel_order(request, id_order, id_user):
    user = request.user
    if user.id != id_user:
        return render(request, '404.html')
    user = request.user
    products_all = OrderItem.objects.filter(order=id_order)

    for i in products_all:
        id_product = i.product.id
        quantity = i.quantity
        cart = Product.objects.get(id=id_product)
        cart.quantity += quantity
        cart.save()

    order = Order.objects.get(id=id_order)
    # Отправка сообщения на почту
    send_email_order(
        request,
        user,
        order,
        'orders/notification_email/cancel_order.html',
        'Заказ отменен'
    )
    order.status = 'Отмена'
    order.save()

    return HttpResponseRedirect(reverse('orders:orderlist', args=(user.id,)))
