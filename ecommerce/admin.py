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


class CartItemDisplay(admin.ModelAdmin):
    list_display = ('cart__cart_id', 'product__product_name', 'quantity', 'created_at')
    search_fields = ('cart__cart_id',)
    ordering = ['-id']


class CartDisplay(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')
    search_fields = ('cart_id',)
    ordering = ['-id']


class ProductVariationDisplay(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')


# Register your models here.w

admin.site.register(models.Category, CategoryDisplay)
admin.site.register(models.Product, ProductDisplay)
admin.site.register(models.CartItem, CartItemDisplay)
admin.site.register(models.Cart, CartDisplay)
admin.site.register(models.ProductVariation, ProductVariationDisplay)
