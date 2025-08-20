# library.py
import json, os
import httpx
from book import Book

class Library:
    API_URL = "https://openlibrary.org/isbn/{isbn}.json"
    AUTHOR_URL = "https://openlibrary.org{key}.json"

    def __init__(self, filename: str = "library.json"):
        self.filename = filename
        self.books: list[Book] = []
        self.load_books()  # açılışta JSON’dan oku

    # ---------- JSON işlemleri ----------
    def save_books(self):
        """Kitap listesini JSON dosyasına kaydeder."""
        data = [b.to_dict() for b in self.books]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_books(self):
        """JSON dosyasından kitap listesini yükler."""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self.books = [Book.from_dict(x) for x in raw]
        else:
            self.save_books()  # yoksa boş dosya oluştur

    # ---------- Kütüphane metodları ----------
    def add_book(self, book_or_isbn: "Book | str"):
        """
        Yeni bir kitap ekler.
        - str verilirse: ISBN üzerinden Open Library API'den veriyi çekip ekler.
        - Book verilirse: Aşama 1 ile uyumluluk için direkt ekler.
        """
        if isinstance(book_or_isbn, Book):
            book = book_or_isbn
            isbn = book.isbn
        else:
            isbn = str(book_or_isbn).strip().replace("-", "")
            if any(b.isbn == isbn for b in self.books):
                raise ValueError("Bu ISBN zaten var.")
            book = self._fetch_book_from_api(isbn)

        # ISBN çakışması kontrolü (Book ile gelmişse de güvence)
        if any(b.isbn == book.isbn for b in self.books):
            raise ValueError("Bu ISBN zaten var.")

        self.books.append(book)
        self.save_books()

    def remove_book(self, isbn: str):
        """ISBN ile kitabı siler."""
        before = len(self.books)
        self.books = [b for b in self.books if b.isbn != isbn]
        if len(self.books) == before:
            raise ValueError("Bu ISBN bulunamadı.")
        self.save_books()

    def list_books(self) -> list[Book]:
        """Tüm kitapları döndürür."""
        return self.books

    def find_book(self, isbn: str) -> "Book | None":
        """ISBN ile kitabı arar, bulursa Book nesnesi döner."""
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    # ---------- Yardımcılar ----------
    def _fetch_book_from_api(self, isbn: str) -> Book:
        """Open Library API'den başlık ve yazar isimlerini çekip Book döndürür."""
        try:
            r = httpx.get(self.API_URL.format(isbn=isbn), timeout=10, follow_redirects=True)
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError("Kitap bulunamadı.") from e
            raise ValueError(f"API hatası: {e.response.status_code}") from e
        except httpx.RequestError as e:
            # ağ/dns/zaman aşımı vb.
            raise ValueError("Ağ hatası: API'ye ulaşılamadı.") from e

        data = r.json()
        title = data.get("title")
        author_names: list[str] = []

        # Open Library /isbn yanıtında authors genelde { "key": "/authors/OLxxxxA" } şeklinde gelir.
        for ref in data.get("authors", []):
            key = (ref or {}).get("key")
            if not key:
                continue
            try:
                ar = httpx.get(self.AUTHOR_URL.format(key=key), timeout=10, follow_redirects=True)
                ar.raise_for_status()
                name = (ar.json() or {}).get("name")
                if name:
                    author_names.append(name)
            except (httpx.RequestError, httpx.HTTPStatusError):
                # Yazar çekilemese de kitabı eklemeye devam edelim.
                continue

        if not title:
            raise ValueError("API yanıtı geçersiz: başlık yok.")

        author = ", ".join(author_names) if author_names else "Bilinmiyor"
        return Book(title=title, author=author, isbn=isbn)

