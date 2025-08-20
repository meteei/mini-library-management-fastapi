# test_api.py
import pytest
from fastapi.testclient import TestClient
from library import Library
from book import Book
import api  # api.py içindeki app ve lib

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Her testte izole bir JSON dosyası kullan
    test_file = tmp_path / "api_test.json"
    api.lib = Library(filename=str(test_file))  # api içindeki global lib'i değiştir

    # Ağ çağrısını sahtele
    def fake_fetch(self, isbn: str) -> Book:
        return Book(title="Sahte Kitap", author="Test Yazar", isbn=isbn)
    monkeypatch.setattr(Library, "_fetch_book_from_api", fake_fetch)

    return TestClient(api.app)

def test_get_books_initial_empty(client):
    r = client.get("/books")
    assert r.status_code == 200
    assert r.json() == []

def test_post_books_adds_and_returns_book(client):
    r = client.post("/books", json={"isbn": "12345"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Sahte Kitap"
    assert data["author"] == "Test Yazar"
    assert data["isbn"] == "12345"

    # Liste artık 1 eleman
    r2 = client.get("/books")
    assert len(r2.json()) == 1

def test_post_duplicate_returns_409(client):
    client.post("/books", json={"isbn": "12345"})
    r = client.post("/books", json={"isbn": "12345"})
    assert r.status_code == 409
    assert "zaten var" in r.json()["detail"]

def test_delete_book_then_empty(client):
    client.post("/books", json={"isbn": "12345"})
    r = client.delete("/books/12345")
    assert r.status_code == 200
    assert r.json()["detail"] == "Silindi"

    r2 = client.get("/books")
    assert r2.json() == []

def test_delete_missing_returns_404(client):
    r = client.delete("/books/00000")
    assert r.status_code == 404
# API testleri - Mini Kütüphane Yönetim Sistemi
