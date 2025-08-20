# Proje Güncellemesi
 # Mini Kütüphane API

## 📌 Proje Açıklaması
Bu proje, kitapları ISBN üzerinden ekleme, silme, listeleme ve arama imkanı sunan bir **mini kütüphane uygulamasıdır**.  
Hem **komut satırı arayüzü (CLI)** hem de **FastAPI tabanlı REST API** içerir.  
Kitap bilgileri [Open Library API](https://openlibrary.org/dev/docs/api/books) üzerinden çekilir ve `library.json` dosyasında saklanır.

---

## 📦 Kurulum

### Repoyu Klonlama
```bash
git clone https://github.com/meteei/mini-library-management-fastapi.git
cd mini-library-management-fastapi

### Bağımlılıkları Yükleme
pip install -r requirements.txt


##🚀 Kullanım(usage)

### Terminal Uygulaması (Aşama 1-2)
```bash
  python main.py

##API Sunucusu (Aşama 3)
  uvicorn api:app --reload


##📚 API Dokümantasyonu

 ### Endpoint'ler

GET / - Ana sayfa
GET /books - Tüm kitapları listeler
POST /books - ISBN ile yeni kitap ekler
DELETE /books/{isbn} - ISBN ile kitap siler


# Kitap ekleme
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{"isbn":"9780321765723"}'


# Kitapları listeleme
curl "http://localhost:8000/books"


# Kitap silme
curl -X DELETE "http://localhost:8000/books/9780321765723"


#Otomatik API Dokümantasyonu

http://localhost:8000/docs - Interactive Swagger UI
http://localhost:8000/redoc - ReDoc dokümantasyon




##🏗️ Proje Yapısı

 mini-library-management-fastapi/
├── api.py           # FastAPI endpoint'leri
├── book.py          # Book sınıfı
├── library.py       # Library sınıfı (JSON işlemleri + API entegrasyonu)
├── main.py          # Terminal arayüzü
├── library.json     # Veri deposu (otomatik oluşur)
├── requirements.txt # Bağımlılıklar
├── tests/           # Test dosyaları
│   ├── test_api.py
│   └── test_library.py
└── README.md        # Bu dosya




##🔧 Teknolojiler

Python 3.8+
FastAPI
HTTPX (Open Library API entegrasyonu)
Pydantic
Uvicorn



## 📋 Yapmanız Gereken Adımlar:

### 1. README.md Dosyasını Oluşturun/Güncelleyin

```bash
# Mevcut README.md'yi yedekleyip yenisiyle değiştirin
cp README.md README_backup.md

 
