from django.db import models


class UserTg(models.Model):
    id_tg = models.BigIntegerField(unique=True)
    first_name = models.CharField()

    class Meta:
        db_table = "user_tg"
        verbose_name = "Пользователь Tg"
        verbose_name_plural = "Пользователи Tg"


class Cart(models.Model):
    user = models.ForeignKey(to=UserTg, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")
    product = models.IntegerField(verbose_name="Продукт")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")

    class Meta:
        db_table = "cart_tg"
        verbose_name = "Корзина Tg"
        verbose_name_plural = "Корзина Tg"


class Order(models.Model):
    user = models.ForeignKey(to=UserTg, on_delete=models.SET_DEFAULT, blank=True, null=True,
                             verbose_name="Пользователь",
                             default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    delivery_address = models.TextField(null=True, blank=True, verbose_name="Адрес доставки")
    status = models.CharField(max_length=50, default='В обработке', choices=(('В обработке', 'В обработке'),
                                                                             ('Отправлено', 'Отправлено'),
                                                                             ('Доставлено', 'Доставлено'),
                                                                             ('Отмена', 'Отмена')),
                              verbose_name="Статус заказа")

    class Meta:
        db_table = "order_tg"
        verbose_name = "Заказ Tg"
        verbose_name_plural = "Заказы Tg"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.IntegerField(verbose_name="Продукт")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")

    class Meta:
        db_table = "order_item_tg"
        verbose_name = "Проданный товар Tg"
        verbose_name_plural = "Проданные товары Tg"
