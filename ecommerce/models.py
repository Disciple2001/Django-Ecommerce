from django.db import models
from django.urls import reverse


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

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-id']
