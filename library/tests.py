import os
import unittest
from unittest.mock import patch
from library.models import Book, DataBase


class TestDataBase(unittest.TestCase):

    def setUp(self):
        self.database = DataBase("test_books.json")
        self.database.create()
        self.database.update_actual_id(self.database)
        self.book = Book("Test Title", "Test Author", 2021, "в наличии")
        self.book.save(self.database)

    def tearDown(self):
        import os
        if os.path.exists("test_books.json"):
            os.remove("test_books.json")

    def test_database_create(self):
        self.assertTrue(os.path.exists("test_books.json"))

    def test_get_all(self):
        books = self.database.get_all()
        self.assertIsInstance(books, list)
        self.assertGreaterEqual(len(books), 1)

    def test_get(self):
        book = self.database.get(1)
        self.assertIsNotNone(book)
        self.assertEqual(book.title, "Test Title")

    def test_delete(self):
        self.database.delete(1)
        self.assertIsNone(self.database.get(1))

    def test_change_status(self):
        self.database.change_status(1, "выдана")
        book = self.database.get(1)
        self.assertEqual(book.status, "выдана")

    def test_search(self):
        result = self.database.search(key_word="Test Title")
        self.assertGreaterEqual(len(result), 1)
        result = self.database.search(year=2021)
        self.assertGreaterEqual(len(result), 1)

    def test_is_exist(self):
        self.assertTrue(self.database.is_exist(self.book))

    @patch('builtins.input', side_effect=["Test Title", "Test Author", "2021", "1"])
    def test_add_book(self, mock_input):
        book = Book("New Title", "New Author", 2022, "в наличии")
        book.save(self.database)
        self.assertTrue(self.database.is_exist(book))
        self.database.delete(1)  # Clean up


class TestBook(unittest.TestCase):

    def setUp(self):
        self.book = Book("Test Title", "Test Author", 2021, "в наличии")

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Title")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.year, 2021)
        self.assertEqual(self.book.status, "в наличии")

    def test_book_str(self):
        self.assertEqual(str(self.book), "Test Title | Test Author | 2021 | в наличии")

    @patch('builtins.input', side_effect=["Test Title", "Test Author", "2021", "1"])
    def test_book_save(self, mock_input):
        database = DataBase("test_books.json")
        database.create()
        result = self.book.save(database)
        self.assertIsInstance(result, Book)
        self.assertTrue(database.is_exist(self.book))
        database.delete(1)  # Clean up


if __name__ == '__main__':
    unittest.main()
