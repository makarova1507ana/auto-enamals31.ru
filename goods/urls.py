from django.urls import path
from .views import catalog,  get_detail_card_by_slug, categories,subcategories, catalog_sub

app_name = 'goods'

urlpatterns = [
    path('', catalog, name='catalog'),
    path('search/', catalog, name='search'),
    path('categories/', categories, name='categories'),
    path('<slug:slug>/catalog/', catalog_sub, name='catalog_sub'),
    path('categories/<slug:slug>/', subcategories, name='subcategories'),
    path('<int:page>/', catalog, name='catalog'),
    path('<slug:slug>/detail/', get_detail_card_by_slug, name='detail_card'),

]
