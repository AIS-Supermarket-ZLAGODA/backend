from django.urls import path
from .views.TestTableListView import TestTableListView
from .views.CategoryView import CategoryListView
from .views.CategoryView import CategoryDetailView
from .views.ProductView import ProductListView
from .views.ProductView import ProductDetailView
from .views.AuthView import LoginView
from .views.EmployeeView import EmployeeListView, EmployeeDetailView
from .views.CheckView import CheckListView, CheckDetailView
from .views.CustomerCardView import CustomerCardListView, CustomerCardDetailView
from .views.StoreProductView import StoreProductListView, StoreProductDetailView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('test-data/', TestTableListView.as_view(), name='test-data-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_number>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:id_product>/', ProductDetailView.as_view(), name='product-detail'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/<str:id_employee>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('checks/', CheckListView.as_view(), name='check-list'),
    path('checks/<str:check_number>/', CheckDetailView.as_view(), name='check-detail'),
    path('customers/', CustomerCardListView.as_view(), name='customer-list'),
    path('customers/<str:card_number>/', CustomerCardDetailView.as_view(), name='customer-detail'),
    path('store-products/', StoreProductListView.as_view(), name='store-product-list'),
    path('store-products/<str:UPC>/', StoreProductDetailView.as_view(), name='store-product-detail'),
]