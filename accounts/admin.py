from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts import models


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'date_joined', 'last_login', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.

admin.site.register(models.CustomUser, CustomUserAdmin)
