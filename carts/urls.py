from django.urls import path
from .views import cart_add, cart_remove, cart_change, corzina, detail_cart_add, cart_select, cart_select_all, \
    cart_select_delete

app_name = 'carts'

urlpatterns = [
    path('corzina/', corzina, name='corzina'),
    path('cart_add/', cart_add, name='cart_add'),
    path('cart_add_detail/', detail_cart_add, name='cart_add_detail'),
    path('cart_remove/', cart_remove, name='cart_remove'),
    path('cart_change/', cart_change, name='cart_change'),
    path('cart_select/', cart_select, name='cart_select'),
    path('cart_select_all/', cart_select_all, name='cart_select_all'),
    path('cart_select_delete/', cart_select_delete, name='cart_select_delete'),
]
