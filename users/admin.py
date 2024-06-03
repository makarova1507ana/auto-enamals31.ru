from django.contrib import admin

from carts.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_login', 'first_name', 'email', 'username', 'email_verify')
    list_display_links = ('id', 'last_login')
    search_fields = ('last_login', 'first_name', 'email')

    inlines = [OrderTabulareAdmin, CartTabAdmin]
