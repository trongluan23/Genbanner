# Changelog - Migration to MVC Architecture

## Ngày: 2026-02-06

### 🎯 Mục tiêu
Tổ chức lại dự án theo mô hình MVC (Model-View-Controller) chuẩn để cải thiện khả năng bảo trì và mở rộng.

---

## 📁 Thay đổi cấu trúc thư mục

### Trước:
```
FlaskProject/
├── website/
│   ├── __init__.py
│   ├── auth.py (chứa tất cả routes)
│   ├── models.py (chứa tất cả models)
│   └── template/
└── untils/ (typo)
    ├── genbanner.py
    ├── processbackground.py
    ├── portrait.py
    ├── square.py
    └── until.py (typo)
```

### Sau:
```
FlaskProject/
├── app/
│   ├── models/          # MODEL layer
│   │   ├── user.py
│   │   └── banner.py
│   ├── views/           # VIEW layer
│   │   └── *.html
│   ├── controllers/     # CONTROLLER layer
│   │   ├── auth_controller.py
│   │   └── banner_controller.py
│   ├── services/        # Business logic
│   │   ├── banner_service.py
│   │   └── file_service.py
│   ├── utils/           # Utilities
│   │   ├── genbanner.py
│   │   ├── processbackground.py
│   │   ├── portrait.py
│   │   ├── square.py
│   │   └── openai_client.py
│   └── config/          # Configuration
│       └── settings.py
└── app.py
```

---

## 🔄 Chi tiết thay đổi

### 1. Models (DATABASE LAYER)
**Trước:** `website/models.py` (1 file chứa tất cả)
```python
class User(db.Model, UserMixin):
    ...
class Banner(db.Model):
    ...
```

**Sau:** Tách thành 2 files riêng biệt
- `app/models/user.py` - User model
- `app/models/banner.py` - Banner model

**Lợi ích:** Dễ quản lý, mỗi model một file riêng

---

### 2. Controllers (REQUEST HANDLERS)
**Trước:** `website/auth.py` (1 file chứa tất cả routes)
- Authentication routes (login, register, logout)
- Banner routes (create, view, history, delete)
- Business logic lẫn lộn với route handlers

**Sau:** Tách thành 2 controllers chuyên biệt
- `app/controllers/auth_controller.py`
  - `/auth/login` - Đăng nhập
  - `/auth/register` - Đăng ký
  - `/auth/logout` - Đăng xuất

- `app/controllers/banner_controller.py`
  - `/` - Trang chủ
  - `/create` - Tạo banner
  - `/history` - Lịch sử
  - `/banner/<id>` - Xem chi tiết
  - `/banner/<id>/delete` - Xóa

**Lợi ích:** 
- Tách biệt concerns
- Controllers chỉ xử lý HTTP requests
- Business logic được chuyển sang Services

---

### 3. Services (BUSINESS LOGIC LAYER) - MỚI
**Trước:** Logic nằm trực tiếp trong controllers

**Sau:** Tạo Services layer riêng
- `app/services/banner_service.py`
  - `create_banner()` - Logic tạo banner
  - `_save_to_database()` - Lưu vào DB
  - `_read_file()` - Đọc file

- `app/services/file_service.py`
  - `save_uploaded_files()` - Xử lý upload
  - `cleanup_banner_files()` - Dọn dẹp files

**Lợi ích:**
- Tách business logic khỏi controllers
- Dễ test và reuse
- Single Responsibility Principle

---

### 4. Views (TEMPLATES)
**Trước:** `website/template/*.html`

**Sau:** `app/views/*.html`

**Thay đổi:** Chỉ di chuyển vị trí, nội dung giữ nguyên

---

### 5. Utils (UTILITIES)
**Trước:** `untils/` (typo trong tên thư mục)
- `until.py` (typo trong tên file)

**Sau:** `app/utils/`
- `openai_client.py` (đổi tên từ until.py)
- Các file khác giữ nguyên tên

**Thay đổi imports:**
```python
# Trước
from untils.until import client
from untils.genbanner import genbanner

# Sau
from app.utils.openai_client import client
from app.utils.genbanner import genbanner
```

---

### 6. Configuration - MỚI
**Trước:** Config nằm rải rác trong `__init__.py`

**Sau:** `app/config/settings.py`
```python
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "hi")
    SQLALCHEMY_DATABASE_URI = ...
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = ...
```

**Lợi ích:** Tập trung config ở một nơi

---

### 7. Application Factory
**Trước:** `website/__init__.py`
```python
def create_app():
    app = Flask(__name__)
    # Setup trực tiếp
    from .auth import auth
    app.register_blueprint(auth)
```

**Sau:** `app/__init__.py`
```python
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    from app.controllers.banner_controller import banner_bp
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(banner_bp)
    app.register_blueprint(auth_bp)
```

---

## 📊 So sánh Data Flow

### Trước (Monolithic):
```
Request → auth.py → genbanner() → Database → Template
         (tất cả logic ở đây)
```

### Sau (MVC + Services):
```
Request → Controller → Service → Utils → Model → View
          (routing)    (logic)   (AI)    (DB)   (display)
```

---

## ✅ Lợi ích của cấu trúc mới

### 1. Separation of Concerns
- **Models**: Chỉ quan tâm đến database structure
- **Views**: Chỉ quan tâm đến presentation
- **Controllers**: Chỉ xử lý HTTP requests/responses
- **Services**: Chứa business logic
- **Utils**: Các hàm tiện ích

### 2. Maintainability
- Dễ tìm code: Biết chính xác file nào chứa logic gì
- Dễ sửa bug: Thay đổi một layer không ảnh hưởng layer khác
- Dễ đọc: Code tổ chức rõ ràng

### 3. Scalability
- Dễ thêm features mới
- Dễ thêm models, controllers, services mới
- Không lo code bị "phình to"

### 4. Testability
- Có thể test từng layer độc lập
- Mock services khi test controllers
- Mock utils khi test services

### 5. Team Collaboration
- Nhiều người có thể làm việc song song
- Ít conflict khi merge code
- Dễ code review

---

## 🔧 Breaking Changes

### Import paths
```python
# CŨ → MỚI
from website import db → from app import db
from website.models import User → from app.models.user import User
from untils.genbanner import genbanner → from app.utils.genbanner import genbanner
```

### URL endpoints
```python
# CŨ → MỚI
url_for('auth.index') → url_for('banner.create')
url_for('auth.login') → url_for('auth.login')  # Giữ nguyên
```

### Blueprint names
- `auth` blueprint: Giữ nguyên prefix `/auth`
- `banner` blueprint: Mới, không có prefix (root `/`)

---

## 📝 Files Created

### New Files:
1. `app/__init__.py` - Application factory
2. `app/models/user.py` - User model
3. `app/models/banner.py` - Banner model
4. `app/controllers/auth_controller.py` - Auth routes
5. `app/controllers/banner_controller.py` - Banner routes
6. `app/services/banner_service.py` - Banner logic
7. `app/services/file_service.py` - File handling
8. `app/config/settings.py` - Configuration
9. `MVC_STRUCTURE.md` - Documentation
10. `MIGRATION_GUIDE.md` - Migration guide
11. `CHANGELOG_MVC.md` - This file

### Modified Files:
1. `app.py` - Updated import from `website` to `app`
2. `app/utils/*.py` - Updated imports

### Moved Files:
1. `untils/*.py` → `app/utils/*.py`
2. `website/template/*.html` → `app/views/*.html`

---

## 🚀 Next Steps

### Immediate:
1. ✅ Test application: `python app.py`
2. ✅ Verify all routes work
3. ✅ Test banner generation
4. ✅ Test authentication

### Optional Improvements:
1. Add unit tests for services
2. Add integration tests for controllers
3. Move OpenAI API key to environment variables
4. Add logging
5. Add error handling middleware
6. Add API documentation

### Cleanup (after testing):
1. Backup old folders: `website/`, `untils/`
2. Delete old folders if everything works
3. Update `.gitignore` if needed

---

## 📚 Documentation

Xem thêm:
- `MVC_STRUCTURE.md` - Chi tiết cấu trúc MVC
- `MIGRATION_GUIDE.md` - Hướng dẫn migration
- `.kiro/steering/structure-mvc.md` - Steering guide mới

---

## 👥 Credits

Migration thực hiện bởi: Kiro AI Assistant
Ngày: 2026-02-06
