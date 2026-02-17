# Hướng Dẫn Deploy Lên Server

## Các Thay Đổi Đã Thực Hiện

### 1. Quản Lý Đường Dẫn File
Đã chuyển từ đường dẫn cục bộ sang đường dẫn tương đối an toàn cho môi trường server:

**Trước:**
```python
os.getcwd()  # Không ổn định trên server
"outputs/file.png"  # Đường dẫn tương đối không rõ ràng
```

**Sau:**
```python
Config.BASE_DIR  # Thư mục gốc của project
Config.UPLOAD_FOLDER  # Thư mục images
Config.OUTPUTS_FOLDER  # Thư mục outputs
```

### 2. Cấu Hình Trong `app/config/settings.py`
```python
class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "images")
    OUTPUTS_FOLDER = os.path.join(BASE_DIR, "outputs")
```

### 3. Tự Động Tạo Thư Mục
Các thư mục cần thiết được tạo tự động khi khởi động app trong `app/__init__.py`:
```python
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.OUTPUTS_FOLDER, exist_ok=True)
```

### 4. File Tạm Thời
Tất cả file tạm thời giờ được lưu trong `outputs/` với tên unique để tránh xung đột:
- `banner_portrait_top_temp.png` → `outputs/banner_portrait_top_temp.png`
- `banner_portrait_bot_temp.png` → `outputs/banner_portrait_bot_temp.png`

## Yêu Cầu Deploy

### 1. Biến Môi Trường (.env)
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host/database
OPENAI_API_KEY=your-openai-api-key
```

### 2. Quyền Truy Cập File
Đảm bảo server có quyền ghi vào các thư mục:
```bash
chmod 755 images/
chmod 755 outputs/
```

### 3. Cấu Trúc Thư Mục
```
project/
├── app/
├── images/          # Tự động tạo
│   └── user_*/      # Tự động tạo cho mỗi user
├── outputs/         # Tự động tạo
├── instance/        # Database
└── .env
```

## Deploy Lên Render/Heroku

### Render
1. Thêm build command:
```bash
pip install -r requirements.txt
```

2. Thêm start command:
```bash
gunicorn app:app
```

3. Thêm environment variables trong Render dashboard

### Heroku
1. Tạo `Procfile`:
```
web: gunicorn app:app
```

2. Set config vars:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-database-url
heroku config:set OPENAI_API_KEY=your-api-key
```

## Lưu Ý Quan Trọng

1. **File Storage**: Trên server như Render/Heroku, file system là ephemeral (tạm thời). Nên sử dụng cloud storage (S3, Cloudinary) cho production.

2. **Database**: Đã cấu hình PostgreSQL. Đảm bảo DATABASE_URL được set đúng.

3. **OpenAI API**: Đảm bảo API key được set trong environment variables.

4. **Memory**: Banner generation tốn nhiều memory. Đảm bảo server có đủ RAM (ít nhất 512MB).

## Kiểm Tra Sau Deploy

1. Kiểm tra thư mục được tạo:
```python
print(Config.BASE_DIR)
print(Config.UPLOAD_FOLDER)
print(Config.OUTPUTS_FOLDER)
```

2. Test upload file
3. Test generate banner
4. Kiểm tra logs để debug nếu có lỗi
