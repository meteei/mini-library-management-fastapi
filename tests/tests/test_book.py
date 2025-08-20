import pytest
from book import Book

class TestBook:
    """Book sınıfı testleri"""
    
    def test_book_creation(self):
        """Book oluşturma testi"""
        book = Book("Test Kitap", "Test Yazar", "1234567890")
        assert book.title == "Test Kitap"
        assert book.author == "Test Yazar"
        assert book.isbn == "1234567890"
    
    def test_to_dict(self):
        """to_dict metod testi"""
        book = Book("Test Kitap", "Test Yazar", "1234567890")
        book_dict = book.to_dict()
        assert book_dict == {
            "title": "Test Kitap",
            "author": "Test Yazar", 
            "isbn": "1234567890"
        }
    
    def test_from_dict(self):
        """from_dict metod testi"""
        book_data = {"title": "Test Kitap", "author": "Test Yazar", "isbn": "1234567890"}
        book = Book.from_dict(book_data)
        assert book.title == "Test Kitap"
        assert book.author == "Test Yazar"
        assert book.isbn == "1234567890"
    
    def test_str_representation(self):
        """__str__ metod testi"""
        book = Book("Test Kitap", "Test Yazar", "1234567890")
        expected_str = "Test Kitap by Test Yazar (ISBN: 1234567890)"
        assert str(book) == expected_str
