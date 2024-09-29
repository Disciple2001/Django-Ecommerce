from django.contrib import admin

from ecommerce import models


class CategoryDisplay(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug', 'created_at')
    search_fields = ('category_name',)


class ProductDisplay(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'category', 'quantity', 'created_at', 'updated_at', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    search_fields = ('product_name',)

# Register your models here.

admin.site.register(models.Category, CategoryDisplay)
admin.site.register(models.Product, ProductDisplay)
