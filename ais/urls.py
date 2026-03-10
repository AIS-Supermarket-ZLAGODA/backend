from django.urls import path
from .views.TestTableListView import TestTableListView
from .views.CategoryView import CategoryListView
from .views.CategoryView import CategoryDetailView
from .views.ProductView import ProductListView
from .views.ProductView import ProductDetailView
from .views.AuthView import LoginView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('test-data/', TestTableListView.as_view(), name='test-data-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_number>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:id_product>/', ProductDetailView.as_view(), name='product-detail'),
]