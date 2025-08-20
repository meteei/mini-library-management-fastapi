# main.py
from book import Book
from library import Library

def main():
    lib = Library()  # library.json otomatik açılır/oluşur

    while True:
        print("\n--- Mini Kütüphane ---")
        print("1) Kitap Ekle (ISBN ile)")
        print("2) Kitap Sil")
        print("3) Kitapları Listele")
        print("4) Kitap Ara (ISBN ile)")
        print("5) Çıkış")
        secim = input("> ").strip()

        if secim == "1":
            isbn = input("ISBN: ").strip()
            try:
                lib.add_book(isbn)  # <- sadece ISBN
                print("✅ Eklendi!")
            except ValueError as e:
                print("⚠️", e)

        elif secim == "2":
            isbn = input("Silmek istediğiniz ISBN: ").strip()
            try:
                lib.remove_book(isbn)
                print("🗑️ Silindi!")
            except ValueError as e:
                print("⚠️", e)

        elif secim == "3":
            books = lib.list_books()
            if not books:
                print("(Henüz kitap yok)")
            for b in books:
                print("-", str(b))

        elif secim == "4":
            isbn = input("Aranacak ISBN: ").strip()
            book = lib.find_book(isbn)
            if book:
                print("📖 Bulundu:", book)
            else:
                print("❌ Bu ISBN yok.")

        elif secim == "5":
            print("👋 Görüşürüz!")
            break

        else:
            print("Lütfen 1-5 arasında bir sayı gir.")

if __name__ == "__main__":
    from api import app
    main()

