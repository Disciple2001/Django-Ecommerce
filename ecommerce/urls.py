from django.urls import path

from ecommerce import views

urlpatterns = [
    path('', views.store, name='store'),
    path('search/', views.search, name='search'),

    path('cart', views.cart, name='cart'),
    path('cart/add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove_product_from_cart/<int:product_id>/<int:cart_id>/', views.remove_product_from_cart, name='remove_product_from_cart'),
    path('cart/decrese_quantity_from_cart_product/<int:product_id>/<int:cart_id>/', views.decrese_quantity_from_cart_product, name='decrese_quantity_from_cart_product'),

    path('<slug:category_slug>/', views.store, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail')
]
