from django.urls import path
from .views import index, about, deliver

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('deliver/', deliver, name='deliver'),

]
