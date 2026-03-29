import unittest
from unittest.mock import MagicMock
from django.db import IntegrityError
from ais.services.CategoryService import CategoryService, _validate_category_name

class TestCategoryService(unittest.TestCase):
    def setUp(self):
        self.service = CategoryService()
        self.service.repository = MagicMock()

    def test_validate_category_name_valid(self):
        name = _validate_category_name("Молочні продукти 1-2'3")
        self.assertEqual(name, "Молочні продукти 1-2'3")

    def test_validate_category_name_invalid_empty(self):
        with self.assertRaises(ValueError):
            _validate_category_name("   ")

    def test_validate_category_name_invalid_chars(self):
        with self.assertRaises(ValueError):
            _validate_category_name("Category?!")

    def test_get_list_of_categories(self):
        self.service.repository.get_all.return_value = []
        result = self.service.get_list_of_categories()
        self.assertEqual(result, [])
        self.service.repository.get_all.assert_called_once()

    def test_check_name_unique_valid(self):
        self.service.repository.get_all.return_value = [{'category_number': 1, 'category_name': 'Meat'}]
        # Should not raise
        self.service._check_name_unique("Dairy")

    def test_check_name_unique_invalid(self):
        self.service.repository.get_all.return_value = [{'category_number': 1, 'category_name': 'Meat'}]
        with self.assertRaises(ValueError):
            self.service._check_name_unique("meat")

    def test_check_name_unique_exclude_id(self):
        self.service.repository.get_all.return_value = [{'category_number': 1, 'category_name': 'Meat'}]
        self.service._check_name_unique("meat", exclude_id=1)

    def test_get_category_by_number_found(self):
        self.service.repository.get_by_number.return_value = {'category_number': 1}
        result = self.service.get_category_by_number(1)
        self.assertEqual(result, {'category_number': 1})

    def test_get_category_by_number_not_found(self):
        self.service.repository.get_by_number.return_value = None
        with self.assertRaises(ValueError):
            self.service.get_category_by_number(99)

    def test_add_category(self):
        self.service.repository.get_all.return_value = []
        self.service.repository.create.return_value = 1
        result = self.service.add_category("Meat")
        self.assertEqual(result, 1)

    def test_update_category(self):
        self.service.repository.get_by_number.return_value = {'category_number': 1}
        self.service.repository.get_all.return_value = []
        result = self.service.update_category(1, "New Meat")
        self.assertEqual(result, {'category_number': 1, 'category_name': 'New Meat'})

    def test_delete_category(self):
        self.service.repository.get_by_number.return_value = {'category_number': 1}
        self.service.delete_category(1)
        self.service.repository.delete.assert_called_with(1)

    def test_delete_category_integrity_error(self):
        self.service.repository.get_by_number.return_value = {'category_number': 1}
        self.service.repository.delete.side_effect = IntegrityError()
        with self.assertRaises(ValueError) as ctx:
            self.service.delete_category(1)
        self.assertIn("Цю категорію неможливо видалити", str(ctx.exception))
