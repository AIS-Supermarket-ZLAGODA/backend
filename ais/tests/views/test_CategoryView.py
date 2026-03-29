from rest_framework.test import APIRequestFactory
from unittest.mock import patch
from django.test import SimpleTestCase
from ais.views.CategoryView import CategoryListView, CategoryDetailView

class TestCategoryView(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('ais.views.CategoryView.CategoryService')
    def test_category_list_get(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.get_list_of_categories.return_value = [{'category_number': 1, 'category_name': 'Meat'}]
        
        request = self.factory.get('/api/categories/')
        view = CategoryListView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{'category_number': 1, 'category_name': 'Meat'}])

    @patch('ais.views.CategoryView.CategoryService')
    def test_category_list_post_valid(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.add_category.return_value = 1
        
        request = self.factory.post('/api/categories/', {'category_name': 'Meat'}, format='json')
        view = CategoryListView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'category_number': 1, 'category_name': 'Meat'})

    @patch('ais.views.CategoryView.CategoryService')
    def test_category_list_post_invalid_validation(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.add_category.side_effect = ValueError("Invalid name")
        
        request = self.factory.post('/api/categories/', {'category_name': 'Meat'}, format='json')
        view = CategoryListView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': 'Invalid name'})

    def test_category_list_post_bad_request(self):
        request = self.factory.post('/api/categories/', {}, format='json')
        view = CategoryListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)

    @patch('ais.views.CategoryView.CategoryService')
    def test_category_detail_get(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.get_category_by_number.return_value = {'category_number': 1, 'category_name': 'Meat'}
        
        request = self.factory.get('/api/categories/1/')
        view = CategoryDetailView.as_view()
        response = view(request, category_number=1)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'category_number': 1, 'category_name': 'Meat'})

    @patch('ais.views.CategoryView.CategoryService')
    def test_category_detail_get_not_found(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.get_category_by_number.side_effect = ValueError("not found")
        
        request = self.factory.get('/api/categories/1/')
        view = CategoryDetailView.as_view()
        response = view(request, category_number=1)
        
        self.assertEqual(response.status_code, 404)

    @patch('ais.views.CategoryView.CategoryService')
    def test_category_detail_put(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.update_category.return_value = {'category_number': 1, 'category_name': 'New Meat'}
        
        request = self.factory.put('/api/categories/1/', {'category_name': 'New Meat'}, format='json')
        view = CategoryDetailView.as_view()
        response = view(request, category_number=1)
        
        self.assertEqual(response.status_code, 200)

    def test_category_detail_put_bad_request(self):
        request = self.factory.put('/api/categories/1/', {}, format='json')
        view = CategoryDetailView.as_view()
        response = view(request, category_number=1)
        self.assertEqual(response.status_code, 400)

    @patch('ais.views.CategoryView.CategoryService')
    def test_category_detail_delete(self, mock_service_class):
        request = self.factory.delete('/api/categories/1/')
        view = CategoryDetailView.as_view()
        response = view(request, category_number=1)
        
        self.assertEqual(response.status_code, 204)
