# api.py
from fastapi import FastAPI

app = FastAPI()
@app.get("/", summary="API kök endpointi")
def root():
    return {"message": "Mini Kütüphane API'ye hoş geldiniz!"}

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from library import Library
from book import Book

app = FastAPI(
    title="Mini Kütüphane API",
    version="1.0.0",
    description="Book/Library sınıflarını REST API olarak sunar."
)

# Tek bir Library örneği (JSON dosyasını yönetir)
lib = Library()  # varsayılan: library.json

# --------- Pydantic Modelleri ---------
class BookOut(BaseModel):
    title: str
    author: str
    isbn: str

    @classmethod
    def from_book(cls, b: Book) -> "BookOut":
        return cls(title=b.title, author=b.author, isbn=b.isbn)

class ISBNIn(BaseModel):
    isbn: str = Field(..., examples=["9780321765723", "0-201-03801-3"])

# --------- Endpoint'ler ---------
@app.get("/books", response_model=List[BookOut], summary="Tüm kitapları listele")
def list_books():
    return [BookOut.from_book(b) for b in lib.list_books()]

@app.post("/books", response_model=BookOut, summary="ISBN ile kitap ekle")
def add_book(payload: ISBNIn):
    isbn = payload.isbn.strip().replace("-", "")
    try:
        lib.add_book(isbn)                      # Aşama 2'deki Open Library çağrısını tetikler
        added = lib.find_book(isbn)
        assert added is not None
        return BookOut.from_book(added)
    except ValueError as e:
        msg = str(e)
        # Basit hata eşlemesi
        if "zaten var" in msg:
            raise HTTPException(status_code=409, detail=msg)
        if "bulunamadı" in msg:
            raise HTTPException(status_code=404, detail=msg)
        # Ağ/API vb. durumlar
        raise HTTPException(status_code=502, detail=msg)

@app.delete("/books/{isbn}", summary="ISBN ile kitabı sil")
def delete_book(isbn: str):
    try:
        lib.remove_book(isbn.strip().replace("-", ""))
        return {"detail": "Silindi"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

# FastAPI ile REST API endpoints
