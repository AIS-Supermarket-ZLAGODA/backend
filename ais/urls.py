from django.urls import path
from .views.TestTableListView import TestTableListView

urlpatterns = [
    path('test-data/', TestTableListView.as_view(), name='test-data-list'),
]