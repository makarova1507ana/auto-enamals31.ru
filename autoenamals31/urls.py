import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from autoenamals31 import settings
from autoenamals31.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('allauth.urls')),
    path('account/', include('social_django.urls', namespace='social')),
    path('', include('main.urls', namespace='main')),
    path('catalog/', include('goods.urls', namespace='catalog')),
    path('user/', include('users.urls', namespace='user')),
    path('cart/', include('carts.urls', namespace='cart')),
    path('order/', include('orders.urls', namespace='orders')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
