# test_library.py
import os
import pytest
from book import Book
from library import Library

TEST_FILE = "test_library.json"

@pytest.fixture
def empty_library():
    """Her test için temiz bir kütüphane sağlar."""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    lib = Library(filename=TEST_FILE)
    yield lib
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_add_book(empty_library):
    book = Book("Test Kitap", "Yazar A", "12345")
    empty_library.add_book(book)
    assert len(empty_library.books) == 1
    assert empty_library.books[0].isbn == "12345"

def test_add_duplicate_book(empty_library):
    book1 = Book("Kitap 1", "Yazar A", "12345")
    book2 = Book("Kitap 2", "Yazar B", "12345")
    empty_library.add_book(book1)
    with pytest.raises(ValueError):
        empty_library.add_book(book2)

def test_remove_book(empty_library):
    book = Book("Test Kitap", "Yazar A", "12345")
    empty_library.add_book(book)
    empty_library.remove_book("12345")
    assert len(empty_library.books) == 0

def test_remove_nonexistent_book(empty_library):
    with pytest.raises(ValueError):
        empty_library.remove_book("99999")

def test_find_book(empty_library):
    book = Book("Test Kitap", "Yazar A", "12345")
    empty_library.add_book(book)
    found = empty_library.find_book("12345")
    assert found is not None
    assert found.title == "Test Kitap"

def test_find_nonexistent_book(empty_library):
    found = empty_library.find_book("99999")
    assert found is None

def test_list_books(empty_library):
    book1 = Book("Kitap 1", "Yazar A", "111")
    book2 = Book("Kitap 2", "Yazar B", "222")
    empty_library.add_book(book1)
    empty_library.add_book(book2)
    books = empty_library.list_books()
    assert len(books) == 2
    assert books[0].isbn == "111"
    assert books[1].isbn == "222"

def test_save_and_load_books(empty_library):
    book = Book("Kitap 1", "Yazar A", "111")
    empty_library.add_book(book)
    new_lib = Library(filename=TEST_FILE)
    assert len(new_lib.books) == 1
    assert new_lib.books[0].isbn == "111"
# Library testleri - Temel işlevsellik testleri
def test_search_books(empty_library):
    """Kitap arama testi - başlık ve yazar arama"""
    book1 = Book("Python Programming", "Guido van Rossum", "11111")
    book2 = Book("Java Programming", "James Gosling", "22222") 
    book3 = Book("Python Cookbook", "David Beazley", "33333")
    
    empty_library.add_book(book1)
    empty_library.add_book(book2)
    empty_library.add_book(book3)
    
    # Başlıkta "Python" arama
    results = empty_library.search_books("Python")
    assert len(results) == 2
    python_titles = [b.title for b in results]
    assert "Python Programming" in python_titles
    assert "Python Cookbook" in python_titles
    
    # Yazar adında "Guido" arama
    results = empty_library.search_books("Guido")
    assert len(results) == 1
    assert results[0].title == "Python Programming"
    
    # Bulunamayan kitap arama
    results = empty_library.search_books("JavaScript")
    assert len(results) == 0

def test_book_str_representation(empty_library):
    """Book __str__ metod testi"""
    book = Book("Test Kitap", "Test Yazar", "12345")
    empty_library.add_book(book)
    expected_str = "Test Kitap by Test Yazar (ISBN: 12345)"
    assert str(empty_library.books[0]) == expected_str

def test_book_to_dict_method(empty_library):
    """Book to_dict metod testi"""
    book = Book("Test Kitap", "Test Yazar", "12345")
    empty_library.add_book(book)
    book_dict = empty_library.books[0].to_dict()
    expected_dict = {
        "title": "Test Kitap",
        "author": "Test Yazar", 
        "isbn": "12345"
    }
    assert book_dict == expected_dict
