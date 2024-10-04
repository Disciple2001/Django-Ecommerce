from django.db import models
from django.urls import reverse

from core import settings


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)
    slug = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=1024, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    class Meta:
        ordering = ['-id']
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
    product_name = models.CharField(max_length=124, unique=True)
    slug = models.SlugField(max_length=124, unique=True)
    description = models.TextField(max_length=1024, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    image = models.ImageField(upload_to='photos/products', blank=True)

    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-id']


class ProductVariationManager(models.Manager):
    def colors(self):
        return super(ProductVariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(ProductVariationManager, self).filter(variation_category='size', is_active=True)


class ProductVariation(models.Model):
    variation_category_choices = (
        ('color', 'color'),
        ('size', 'size'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=124, choices=variation_category_choices)
    variation_value = models.CharField(max_length=124)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ProductVariationManager()

    def __str__(self):
        return f'{self.product.product_name} - {self.variation_category} - {self.variation_value}'

    class Meta:
        verbose_name = 'Product Variation'
        verbose_name_plural = 'Product Variations'
        # ordering = ['-id']


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    variations = models.ManyToManyField(ProductVariation, blank=True)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.product_name}'

    def sub_total(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        ordering = ['-id']
