from rest_framework.test import APIRequestFactory
from unittest.mock import patch
from django.test import SimpleTestCase
from ais.views.ProductView import ProductListView, ProductDetailView

class TestProductView(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('ais.views.ProductView.ProductService')
    def test_product_list_get(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.get_list_of_products.return_value = [{'id_product': 1, 'product_name': 'Milk'}]
        
        request = self.factory.get('/api/products/')
        view = ProductListView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{'id_product': 1, 'product_name': 'Milk'}])
        mock_service.get_list_of_products.assert_called_with(category_name=None, product_name=None)

    @patch('ais.views.ProductView.ProductService')
    def test_product_list_post_valid(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.add_product.return_value = 1
        
        data = {
            'category_number': 1,
            'product_name': 'Milk',
            'producer': 'Farm',
            'characteristics': 'Tasty'
        }
        request = self.factory.post('/api/products/', data, format='json')
        view = ProductListView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, 201)

    @patch('ais.views.ProductView.ProductService')
    def test_product_list_post_invalid(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.add_product.side_effect = ValueError("Invalid")
        
        data = {
            'category_number': 1,
            'product_name': 'Milk',
            'producer': 'Farm',
            'characteristics': 'Tasty'
        }
        request = self.factory.post('/api/products/', data, format='json')
        view = ProductListView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, 400)
        
    def test_product_list_post_bad_request(self):
        request = self.factory.post('/api/products/', {}, format='json')
        view = ProductListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)

    @patch('ais.views.ProductView.ProductService')
    def test_product_detail_get(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.get_product_by_id.return_value = {'id_product': 1}
        
        request = self.factory.get('/api/products/1/')
        view = ProductDetailView.as_view()
        response = view(request, id_product=1)
        
        self.assertEqual(response.status_code, 200)

    @patch('ais.views.ProductView.ProductService')
    def test_product_detail_put(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.update_product.return_value = {'id_product': 1}
        
        data = {
            'category_number': 1,
            'product_name': 'Milk',
            'producer': 'Farm',
            'characteristics': 'Tasty',
            'id_product': 1
        }
        request = self.factory.put('/api/products/1/', data, format='json')
        view = ProductDetailView.as_view()
        response = view(request, id_product=1)
        
        self.assertEqual(response.status_code, 200)

    def test_product_detail_put_bad_request(self):
        request = self.factory.put('/api/products/1/', {}, format='json')
        view = ProductDetailView.as_view()
        response = view(request, id_product=1)
        self.assertEqual(response.status_code, 400)

    @patch('ais.views.ProductView.ProductService')
    def test_product_detail_delete(self, mock_service_class):
        mock_service = mock_service_class.return_value
        
        request = self.factory.delete('/api/products/1/')
        view = ProductDetailView.as_view()
        response = view(request, id_product=1)
        
        self.assertEqual(response.status_code, 204)
