import unittest
from unittest.mock import MagicMock
from django.db import IntegrityError
from ais.services.ProductService import ProductService, _validate_text_field

class TestProductService(unittest.TestCase):
    def setUp(self):
        self.service = ProductService()
        self.service.product_repo = MagicMock()
        self.service.category_service = MagicMock()

    def test_validate_text_field_valid(self):
        result = _validate_text_field("Valid text 1.2,3-4'5", "Field")
        self.assertEqual(result, "Valid text 1.2,3-4'5")

    def test_validate_text_field_invalid(self):
        with self.assertRaises(ValueError):
            _validate_text_field("", "Field")
        with self.assertRaises(ValueError):
            _validate_text_field("Invalid#%", "Field")

    def test_get_list_of_products(self):
        self.service.product_repo.get_all.return_value = []
        result = self.service.get_list_of_products()
        self.assertEqual(result, [])

    def test_get_list_of_products_by_category(self):
        self.service.product_repo.get_by_category_name.return_value = []
        result = self.service.get_list_of_products(category_name="Cat")
        self.assertEqual(result, [])
        self.service.product_repo.get_by_category_name.assert_called_with("Cat")

    def test_get_list_of_products_by_name(self):
        self.service.product_repo.get_by_name.return_value = []
        result = self.service.get_list_of_products(product_name="Prod")
        self.assertEqual(result, [])
        self.service.product_repo.get_by_name.assert_called_with("Prod")

    def test_check_name_unique(self):
        self.service.product_repo.get_all.return_value = [{'id_product': 1, 'product_name': 'Milk'}]
        self.service._check_name_unique("Bread")
        with self.assertRaises(ValueError):
            self.service._check_name_unique("milk")
            
    def test_check_name_unique_exclude_id(self):
        self.service.product_repo.get_all.return_value = [{'id_product': 1, 'product_name': 'Milk'}]
        self.service._check_name_unique("milk", exclude_id=1)

    def test_get_product_by_id(self):
        self.service.product_repo.get_by_id.return_value = {'id_product': 1}
        result = self.service.get_product_by_id(1)
        self.assertEqual(result, {'id_product': 1})
        
    def test_get_product_by_id_not_found(self):
        self.service.product_repo.get_by_id.return_value = None
        with self.assertRaises(ValueError):
            self.service.get_product_by_id(99)

    def test_add_product(self):
        self.service.product_repo.get_all.return_value = []
        self.service.product_repo.create.return_value = 1
        result = self.service.add_product(1, "Milk", "Farm", "Tasty")
        self.assertEqual(result, 1)

    def test_update_product(self):
        self.service.product_repo.get_by_id.return_value = {'id_product': 1}
        self.service.product_repo.get_all.return_value = []
        result = self.service.update_product(1, 1, "Milk", "Farm", "Tasty")
        self.assertEqual(result['product_name'], "Milk")

    def test_delete_product(self):
        self.service.product_repo.get_by_id.return_value = {'id_product': 1}
        self.service.delete_product(1)
        self.service.product_repo.delete.assert_called_with(1)

    def test_delete_product_integrity_error(self):
        self.service.product_repo.get_by_id.return_value = {'id_product': 1}
        self.service.product_repo.delete.side_effect = IntegrityError()
        with self.assertRaises(ValueError):
            self.service.delete_product(1)
