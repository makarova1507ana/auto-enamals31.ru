from django.contrib import admin

from goods.models import Categories, Product, Subcategory, Color, Brand, SubSubcategory


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_image', 'price',)
    list_editable = ('url_image',)
    list_filter = ["category", "subcategory"]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubSubcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Color)
class ColorsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
