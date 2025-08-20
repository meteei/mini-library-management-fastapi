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
