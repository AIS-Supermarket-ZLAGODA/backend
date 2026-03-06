from django.urls import path
from .views.TestTableListView import TestTableListView
from .views.CategoryView import CategoryListView
from .views.CategoryView import CategoryDetailView

urlpatterns = [
    path('test-data/', TestTableListView.as_view(), name='test-data-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_number>/', CategoryDetailView.as_view(), name='category-detail'),
]