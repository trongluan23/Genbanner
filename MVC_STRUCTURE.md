# Cấu trúc MVC - Banner Generation Application

## Tổng quan

Dự án đã được tổ chức lại theo mô hình MVC (Model-View-Controller) chuẩn để dễ bảo trì và mở rộng.

## Cấu trúc thư mục

```
FlaskProject/
├── app/                          # Thư mục ứng dụng chính
│   ├── __init__.py              # Flask application factory
│   ├── models/                   # MODEL - Database models
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   └── banner.py            # Banner model
│   ├── views/                    # VIEW - HTML templates
│   │   ├── base.html            # Base template
│   │   ├── home.html            # Landing page
│   │   ├── index.html           # Banner creation form
│   │   ├── banner.html          # Banner display
│   │   ├── history.html         # Banner history
│   │   ├── login.html           # Login page
│   │   ├── register.html        # Registration page
│   │   └── edit.html            # Edit page
│   ├── controllers/              # CONTROLLER - Request handlers
│   │   ├── __init__.py
│   │   ├── auth_controller.py   # Authentication logic
│   │   └── banner_controller.py # Banner CRUD operations
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── banner_service.py    # Banner generation logic
│   │   └── file_service.py      # File upload/management
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── genbanner.py         # Banner generation orchestrator
│   │   ├── processbackground.py # Background processing
│   │   ├── portrait.py          # Portrait banner generation
│   │   ├── square.py            # Square banner generation
│   │   └── openai_client.py     # OpenAI API client
│   └── config/                   # Configuration
│       ├── __init__.py
│       └── settings.py          # App configuration
├── images/                       # Uploaded images
├── outputs/                      # Generated banners
├── instance/                     # Database files
├── app.py                        # Application entry point
├── requirements.txt              # Python dependencies
└── .env                          # Environment variables
```

## Giải thích các thành phần

### 1. MODEL (app/models/)
Định nghĩa cấu trúc dữ liệu và tương tác với database.

- **user.py**: Model User với các trường email, username, password
- **banner.py**: Model Banner lưu thông tin banner đã tạo

### 2. VIEW (app/views/)
Các template HTML hiển thị giao diện người dùng.

- **base.html**: Template gốc chứa layout chung
- **index.html**: Form tạo banner
- **banner.html**: Hiển thị banner đã tạo
- **history.html**: Lịch sử banner của user
- **login.html/register.html**: Xác thực người dùng

### 3. CONTROLLER (app/controllers/)
Xử lý request từ user và điều phối logic.

- **auth_controller.py**: 
  - `/auth/login` - Đăng nhập
  - `/auth/register` - Đăng ký
  - `/auth/logout` - Đăng xuất

- **banner_controller.py**:
  - `/` - Trang chủ
  - `/create` - Tạo banner mới
  - `/history` - Xem lịch sử
  - `/banner/<id>` - Xem chi tiết banner
  - `/banner/<id>/delete` - Xóa banner

### 4. SERVICES (app/services/)
Business logic và xử lý phức tạp.

- **banner_service.py**: Logic tạo banner, lưu database
- **file_service.py**: Xử lý upload và quản lý file

### 5. UTILS (app/utils/)
Các hàm tiện ích và xử lý AI.

- **genbanner.py**: Điều phối quá trình tạo banner
- **processbackground.py**: Xử lý background với OpenAI
- **portrait.py**: Tạo banner dọc
- **square.py**: Tạo banner vuông
- **openai_client.py**: Cấu hình OpenAI API

### 6. CONFIG (app/config/)
Cấu hình ứng dụng.

- **settings.py**: Database, secret key, upload settings

## Luồng xử lý (Data Flow)

```
1. User gửi request → Controller
2. Controller gọi Service để xử lý logic
3. Service sử dụng Utils để tạo banner
4. Service lưu vào Model/Database
5. Controller trả về View với dữ liệu
```

### Ví dụ: Tạo banner mới

```
POST /create
    ↓
banner_controller.create_post()
    ↓
FileService.save_uploaded_files()  # Lưu file upload
    ↓
BannerService.create_banner()      # Tạo banner
    ↓
genbanner()                        # Điều phối AI
    ↓
processbackground() + portrait/square()  # Xử lý AI
    ↓
Banner.save()                      # Lưu database
    ↓
render_template('banner.html')     # Hiển thị kết quả
```

## Ưu điểm của cấu trúc MVC

1. **Tách biệt trách nhiệm**: Mỗi layer có nhiệm vụ riêng
2. **Dễ bảo trì**: Thay đổi một phần không ảnh hưởng phần khác
3. **Dễ test**: Có thể test từng layer độc lập
4. **Dễ mở rộng**: Thêm tính năng mới dễ dàng
5. **Code sạch hơn**: Logic được tổ chức rõ ràng

## Migration từ cấu trúc cũ

### Thay đổi chính:

1. **website/** → **app/**
2. **untils/** → **app/utils/** (sửa typo)
3. **website/auth.py** → Tách thành:
   - **app/controllers/auth_controller.py** (authentication)
   - **app/controllers/banner_controller.py** (banner operations)
4. **website/models.py** → Tách thành:
   - **app/models/user.py**
   - **app/models/banner.py**
5. Thêm **app/services/** cho business logic
6. Thêm **app/config/** cho configuration

## Chạy ứng dụng

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy development server
python app.py
```

Ứng dụng sẽ chạy tại: http://localhost:5000

## Lưu ý

- File `.env` cần có `SECRET_KEY` và `DATABASE_URL`
- OpenAI API key được cấu hình trong `app/utils/openai_client.py`
- Database tự động tạo khi chạy lần đầu
- Thư mục `images/` và `outputs/` cần có quyền ghi
