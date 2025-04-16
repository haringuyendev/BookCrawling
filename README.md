# 📚 Book Crawler API with FastAPI

Dự án này bao gồm một trình crawl sách và một API sử dụng FastAPI để hiển thị thông tin sách đã thu thập. Dữ liệu được lưu vào thư mục `data`.

---
## ✅ Cấu hình

- Python > 3.12.

## ⚙️ Hướng dẫn sử dụng

### 1. Tạo môi trường ảo

```bash
python3 -m venv .venv
```

### 2. Kích hoạt môi trường ảo

- **Linux / macOS**:

```bash
source .venv/bin/activate
```

- **Windows**:

```bash
.venv\Scripts\activate
```

---

### 3. Tạo file `.env`

Tạo một file `.env` ở thư mục gốc và thêm các biến môi trường:

```env
# Ví dụ 
SECRET_KEY=your_very_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

BOOK_SCRAPE_URL="https://books.toscrape.com/catalogue/"
BOOKS_FILE = "data/books.json"
BOOKS_WITH_COUNTRY_FILE = "data/books_with_country.json"

USERS_FILE = "users.json"
```

---

### 4. Cài đặt thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

---

### 5. Crawl dữ liệu sách

Chạy script để crawl dữ liệu và lưu vào thư mục `data`:

```bash
python3 run_scripts.py
```

---

### 6. Chạy API

Di chuyển vào thư mục `src`:

```bash
cd src
```

Chạy server FastAPI:

```bash
uvicorn main:app --reload
```

---

### 7. Truy cập tài liệu Swagger để test API

Mở trình duyệt và truy cập địa chỉ sau:

```
http://localhost:8000/docs
```

Tại đây, bạn có thể thử nghiệm các endpoint API một cách trực quan thông qua Swagger UI.

---

## 📁 Cấu trúc thư mục

```
.
├── .venv/                      # Môi trường ảo 
├── .env                        # File cấu hình môi trường
├── html_backup/                # Thư mục html_backup
├── logs/                       # Thư mục chứa log của dự án
├── data/                       # Thư mục chứa dữ liệu sách sau khi crawl
│   └── books.json
│   └── books_with_country.json
├── run_scripts.py              # Script để crawl sách
├── users.json                  # User Data
├── requirements.txt            # Danh sách thư viện phụ thuộc
├── README.md                   # Tài liệu hướng dẫn
└── src/                        # Source code FastAPI
    ├── main.py
    ├── auth.py
    ├── controllers/
    ├── models/
    └── ...
```

---

## ✅ Lưu ý

- Đảm bảo Python 3.12 trở lên đã được cài đặt.
- Không push thư mục `.venv` và file `.env` lên Git. Hãy sử dụng `.gitignore`.
- Kiểm tra file `books.json` sau khi crawl để đảm bảo dữ liệu đã được lưu đúng.

---

Chúc bạn sử dụng dự án hiệu quả! 🚀