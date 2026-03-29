import unittest
from unittest.mock import patch, MagicMock
from ais.repositories.CategoryRepository import CategoryRepository

class TestCategoryRepository(unittest.TestCase):
    @patch('ais.repositories.CategoryRepository.connection')
    def test_get_all(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.description = [('category_number',), ('category_name',)]
        mock_cursor.fetchall.return_value = [(1, 'Meat'), (2, 'Dairy')]

        result = CategoryRepository.get_all()

        self.assertEqual(result, [
            {'category_number': 1, 'category_name': 'Meat'},
            {'category_number': 2, 'category_name': 'Dairy'}
        ])
        mock_cursor.execute.assert_called_once_with("SELECT category_number, category_name FROM Category ORDER BY category_name;")

    @patch('ais.repositories.CategoryRepository.connection')
    def test_create(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [10]

        result = CategoryRepository.create("Sweets")

        self.assertEqual(result, 10)
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO Category (category_name) VALUES (%s) RETURNING category_number;",
            ["Sweets"]
        )

    @patch('ais.repositories.CategoryRepository.connection')
    def test_delete(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        CategoryRepository.delete(1)

        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM Category WHERE category_number = %s;",
            [1]
        )

    @patch('ais.repositories.CategoryRepository.connection')
    def test_update(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        CategoryRepository.update(1, "Meat")

        mock_cursor.execute.assert_called_once_with(
            "UPDATE Category SET category_name = %s WHERE category_number = %s;",
            ["Meat", 1]
        )

    @patch('ais.repositories.CategoryRepository.connection')
    def test_get_by_number(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.description = [('category_number',), ('category_name',)]
        mock_cursor.fetchone.return_value = (1, 'Meat')

        result = CategoryRepository.get_by_number(1)

        self.assertEqual(result, {'category_number': 1, 'category_name': 'Meat'})
        mock_cursor.execute.assert_called_once_with(
            "SELECT category_number, category_name FROM Category WHERE category_number = %s;",
            [1]
        )

    @patch('ais.repositories.CategoryRepository.connection')
    def test_get_by_number_not_found(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        result = CategoryRepository.get_by_number(99)

        self.assertIsNone(result)
