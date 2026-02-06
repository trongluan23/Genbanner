# AI Banner Generator - MVC Architecture

## 🎉 Cấu trúc MVC đã hoàn thành!

Dự án đã được tổ chức lại thành công theo mô hình MVC (Model-View-Controller) chuẩn.

---

## 📁 Cấu trúc mới

```
FlaskProject/
├── app/                          # Ứng dụng chính
│   ├── __init__.py              # Application factory
│   ├── models/                   # 📊 MODEL - Database
│   │   ├── user.py              # User model
│   │   └── banner.py            # Banner model
│   ├── views/                    # 🎨 VIEW - Templates
│   │   ├── base.html            # Base layout
│   │   ├── home.html            # Landing page
│   │   ├── index.html           # Banner creation form
│   │   ├── banner.html          # Banner display
│   │   ├── history.html         # Banner history
│   │   ├── login.html           # Login page
│   │   └── register.html        # Registration page
│   ├── controllers/              # 🎮 CONTROLLER - Routes
│   │   ├── auth_controller.py   # Authentication
│   │   └── banner_controller.py # Banner operations
│   ├── services/                 # 💼 SERVICES - Business logic
│   │   ├── banner_service.py    # Banner generation
│   │   └── file_service.py      # File handling
│   ├── utils/                    # 🔧 UTILITIES - Helpers
│   │   ├── genbanner.py         # Banner orchestrator
│   │   ├── processbackground.py # Background processing
│   │   ├── portrait.py          # Portrait banners
│   │   ├── square.py            # Square banners
│   │   └── openai_client.py     # OpenAI API
│   └── config/                   # ⚙️ CONFIG
│       └── settings.py          # Configuration
├── images/                       # Uploaded images
├── outputs/                      # Generated banners
├── instance/                     # Database
├── app.py                        # Entry point
├── test_structure.py             # Test script
└── requirements.txt              # Dependencies
```

---

## 🚀 Chạy ứng dụng

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Cấu hình environment
Tạo file `.env`:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
OPENAI_API_KEY=your-openai-api-key
```

### 3. Chạy test
```bash
python test_structure.py
```

### 4. Khởi động server
```bash
python app.py
```

Truy cập: http://localhost:5000

---

## 📊 Luồng xử lý MVC

```
User Request
    ↓
🎮 CONTROLLER (banner_controller.py)
    ↓
💼 SERVICE (banner_service.py)
    ↓
🔧 UTILS (genbanner.py → AI processing)
    ↓
📊 MODEL (Banner.save())
    ↓
🎨 VIEW (render template)
    ↓
Response to User
```

---

## 🔄 So sánh với cấu trúc cũ

### Trước (Monolithic):
- ❌ Tất cả logic trong 1 file `auth.py`
- ❌ Models lẫn lộn trong 1 file
- ❌ Khó bảo trì và mở rộng
- ❌ Typo trong tên thư mục (`untils`, `until.py`)

### Sau (MVC):
- ✅ Tách biệt rõ ràng: Models, Views, Controllers
- ✅ Thêm Services layer cho business logic
- ✅ Dễ test từng component
- ✅ Dễ thêm features mới
- ✅ Code sạch và có tổ chức

---

## 📝 Routes mới

### Authentication (`/auth/*`)
- `GET /auth/login` - Trang đăng nhập
- `POST /auth/login` - Xử lý đăng nhập
- `GET /auth/register` - Trang đăng ký
- `POST /auth/register` - Xử lý đăng ký
- `GET /auth/logout` - Đăng xuất

### Banner Operations (`/*`)
- `GET /` - Trang chủ
- `GET /create` - Form tạo banner (requires login)
- `POST /create` - Xử lý tạo banner (requires login)
- `GET /history` - Lịch sử banner (requires login)
- `GET /banner/<id>` - Xem chi tiết banner (requires login)
- `GET /banner/<id>/image` - Lấy ảnh banner (requires login)
- `POST /banner/<id>/delete` - Xóa banner (requires login)

---

## 🧪 Test Results

```
✅ File Structure: PASS
✅ Imports: PASS
✅ App Creation: PASS
✅ Blueprints: PASS
✅ Routes: PASS
✅ Database: PASS

🎉 All tests passed!
```

---

## 📚 Documentation

- **MVC_STRUCTURE.md** - Chi tiết cấu trúc MVC
- **MIGRATION_GUIDE.md** - Hướng dẫn migration
- **CHANGELOG_MVC.md** - Lịch sử thay đổi
- **.kiro/steering/structure-mvc.md** - Steering guide

---

## 🎯 Lợi ích

### 1. Separation of Concerns
Mỗi layer có trách nhiệm riêng biệt:
- **Models**: Database structure
- **Views**: Presentation
- **Controllers**: HTTP handling
- **Services**: Business logic
- **Utils**: Helper functions

### 2. Maintainability
- Dễ tìm code
- Dễ sửa bug
- Dễ đọc hiểu

### 3. Scalability
- Dễ thêm features
- Dễ thêm models/controllers mới
- Không lo code "phình to"

### 4. Testability
- Test từng layer độc lập
- Mock services khi test controllers
- Mock utils khi test services

### 5. Team Collaboration
- Nhiều người làm việc song song
- Ít conflict khi merge
- Dễ code review

---

## 🔧 Tech Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Flask-Login** - Authentication
- **PostgreSQL** - Database (production)
- **SQLite** - Database (development)

### AI/Image Processing
- **OpenAI API** - GPT image editing
- **OpenCV** - Image processing
- **NumPy** - Array operations

### Frontend
- **Bootstrap 5** - UI framework
- **Bootstrap Icons** - Icons
- **Vanilla JavaScript** - Interactivity

---

## 🛠️ Next Steps

### Immediate
- [x] Tổ chức lại cấu trúc MVC
- [x] Test tất cả routes
- [x] Cập nhật documentation

### Optional Improvements
- [ ] Add unit tests cho services
- [ ] Add integration tests
- [ ] Thêm logging system
- [ ] Thêm error handling middleware
- [ ] API documentation (Swagger)
- [ ] Docker containerization
- [ ] CI/CD pipeline

### Cleanup
- [ ] Backup thư mục `website/` và `untils/`
- [ ] Xóa thư mục cũ sau khi test kỹ
- [ ] Cập nhật `.gitignore`

---

## 👥 Contributors

Migration thực hiện bởi: **Kiro AI Assistant**  
Ngày: **2026-02-06**

---

## 📄 License

© 2026 AI Banner Generator. All rights reserved.

---

## 🆘 Support

Nếu gặp vấn đề, xem:
1. **TROUBLESHOOTING.md** - Giải quyết lỗi thường gặp
2. **MIGRATION_GUIDE.md** - Hướng dẫn migration chi tiết
3. **test_structure.py** - Chạy test để kiểm tra

---

**Happy Coding! 🚀**
