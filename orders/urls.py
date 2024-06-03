from django.urls import path
from orders.views import order_, create_order, orderlist, get_detail_order_by_id, cancel_order

app_name = 'orders'

urlpatterns = [
    path('', order_, name='order'),
    path('data', create_order, name='order-input'),
    path('<int:id_user>/orderlist', orderlist, name='orderlist'),
    path('<int:id_user>/<int:id_order>/detail-order/', get_detail_order_by_id, name='detail-order'),
    path('<int:id_user>/<int:id_order>/cancel-order/', cancel_order, name='cancel_order'),
]
