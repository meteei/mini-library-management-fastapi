# book.py
class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn  # benzersiz kimlik

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

    def to_dict(self) -> dict:
        """Book nesnesini JSON için sözlüğe çevirir."""
        return {"title": self.title, "author": self.author, "isbn": self.isbn}

    @classmethod
    def from_dict(cls, data: dict):
        """JSON’dan Book nesnesi oluşturur."""
        return cls(data["title"], data["author"], data["isbn"])

