from django.contrib import admin
from carts.models import Cart


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = ("product", "quantity", "created_timestamp",)
    list_display = ["created_timestamp", ]
    search_fields = "product", "quantity", "created_timestamp"
    readonly_fields = ("created_timestamp",)
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user_display", "product_display", "quantity", "created_timestamp", ]
    list_filter = ["created_timestamp", "user", "product__name", ]

    def user_display(self, obj):
        if obj.user:
            user = f'{obj.user.last_name} {obj.user.first_name}'
            return user
        return "Анонимный пользователь"

    def product_display(self, obj):
        return str(obj.product.name)
