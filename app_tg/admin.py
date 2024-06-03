from django.contrib import admin

from app_tg.models import UserTg


@admin.register(UserTg)
class ColorsAdmin(admin.ModelAdmin):
    pass
