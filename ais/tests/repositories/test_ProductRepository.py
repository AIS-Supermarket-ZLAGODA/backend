import unittest
from unittest.mock import patch, MagicMock
from ais.repositories.ProductRepository import ProductRepository

class TestProductRepository(unittest.TestCase):
    @patch('ais.repositories.ProductRepository.connection')
    def test_get_all(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.description = [
            ('id_product',), ('category_number',), ('product_name',), ('producer',), ('characteristics',)
        ]
        mock_cursor.fetchall.return_value = [(1, 10, 'Milk', 'Farm', 'Tasty')]

        result = ProductRepository.get_all()

        self.assertEqual(result, [{'id_product': 1, 'category_number': 10, 'product_name': 'Milk', 'producer': 'Farm', 'characteristics': 'Tasty'}])
        mock_cursor.execute.assert_called_once()

    @patch('ais.repositories.ProductRepository.connection')
    def test_get_by_name(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.description = [
            ('id_product',), ('category_number',), ('product_name',), ('producer',), ('characteristics',)
        ]
        mock_cursor.fetchall.return_value = [(1, 10, 'Milk', 'Farm', 'Tasty')]

        result = ProductRepository.get_by_name("Milk")

        self.assertEqual(result, [{'id_product': 1, 'category_number': 10, 'product_name': 'Milk', 'producer': 'Farm', 'characteristics': 'Tasty'}])
        mock_cursor.execute.assert_called_once()
        
    @patch('ais.repositories.ProductRepository.connection')
    def test_get_by_category_name(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.description = [
            ('id_product',), ('category_number',), ('product_name',), ('producer',), ('characteristics',)
        ]
        mock_cursor.fetchall.return_value = [(1, 10, 'Cheese', 'Farm', 'Tasty')]

        result = ProductRepository.get_by_category_name("Dairy")

        self.assertEqual(result, [{'id_product': 1, 'category_number': 10, 'product_name': 'Cheese', 'producer': 'Farm', 'characteristics': 'Tasty'}])
        mock_cursor.execute.assert_called_once()

    @patch('ais.repositories.ProductRepository.connection')
    def test_create(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]

        result = ProductRepository.create(10, "Milk", "Farm", "Tasty")

        self.assertEqual(result, 1)

    @patch('ais.repositories.ProductRepository.connection')
    def test_delete(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        ProductRepository.delete(1)

        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM Product WHERE id_product = %s;", [1]
        )

    @patch('ais.repositories.ProductRepository.connection')
    def test_update(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        ProductRepository.update(1, 10, "Milk", "Farm", "Tasty")

        mock_cursor.execute.assert_called_once()

    @patch('ais.repositories.ProductRepository.connection')
    def test_get_by_id(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.description = [
            ('id_product',), ('category_number',), ('product_name',), ('producer',), ('characteristics',)
        ]
        mock_cursor.fetchone.return_value = (1, 10, 'Milk', 'Farm', 'Tasty')

        result = ProductRepository.get_by_id(1)

        self.assertEqual(result, {'id_product': 1, 'category_number': 10, 'product_name': 'Milk', 'producer': 'Farm', 'characteristics': 'Tasty'})
        mock_cursor.execute.assert_called_once()

    @patch('ais.repositories.ProductRepository.connection')
    def test_get_by_id_not_found(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        result = ProductRepository.get_by_id(99)

        self.assertIsNone(result)
