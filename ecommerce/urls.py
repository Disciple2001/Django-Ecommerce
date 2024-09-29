from django.urls import path

from ecommerce import views

urlpatterns = [
    path('', views.store, name='store'),

    path('<slug:category_slug>/', views.store, name='products_by_category')
]
