# Hướng dẫn Migration sang cấu trúc MVC

## Các bước đã hoàn thành ✅

1. ✅ Tạo cấu trúc thư mục MVC mới
2. ✅ Di chuyển Models (User, Banner)
3. ✅ Tách Controllers (Auth, Banner)
4. ✅ Tạo Services layer (BannerService, FileService)
5. ✅ Di chuyển Utils (genbanner, processbackground, portrait, square)
6. ✅ Di chuyển Views (templates)
7. ✅ Cập nhật imports trong các file
8. ✅ Cập nhật app.py entry point

## Cấu trúc mới

```
app/
├── models/          ← Database models (User, Banner)
├── views/           ← HTML templates
├── controllers/     ← Request handlers (auth, banner)
├── services/        ← Business logic (banner generation, file handling)
├── utils/           ← Utilities (AI processing, OpenAI client)
└── config/          ← Configuration (settings)
```

## Import changes

### Trước (Old):
```python
from website import db
from website.models import User, Banner
from untils.genbanner import genbanner
from untils.until import client
```

### Sau (New):
```python
from app import db
from app.models.user import User
from app.models.banner import Banner
from app.utils.genbanner import genbanner
from app.utils.openai_client import client
```

## Các file cần cập nhật thủ công (nếu có)

### 1. Templates (app/views/)
Nếu có hardcoded paths, cần cập nhật:
- `url_for('auth.login')` → Giữ nguyên
- `url_for('banner.create')` → Thay vì `auth.index`

### 2. Environment variables (.env)
Đảm bảo có:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
OPENAI_API_KEY=your-openai-key
```

### 3. OpenAI Client (app/utils/openai_client.py)
Cập nhật để đọc từ environment:
```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
```

## Testing

### 1. Test imports
```bash
python -c "from app import create_app; print('OK')"
```

### 2. Test database
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('DB OK')"
```

### 3. Run application
```bash
python app.py
```

## Rollback (nếu cần)

Nếu gặp vấn đề, có thể quay lại cấu trúc cũ:
1. Thư mục `website/` vẫn còn nguyên
2. Thư mục `untils/` đã được copy sang `app/utils/`
3. Chỉ cần đổi import trong `app.py` về `from website import create_app`

## Cleanup (sau khi test thành công)

Sau khi đảm bảo mọi thứ hoạt động tốt, có thể xóa:
```bash
# Backup trước khi xóa
mkdir backup
xcopy /E /I website backup\website
xcopy /E /I untils backup\untils

# Xóa thư mục cũ
rmdir /S /Q website
rmdir /S /Q untils
```

## Lợi ích của cấu trúc mới

1. **Separation of Concerns**: Mỗi layer có trách nhiệm riêng
2. **Maintainability**: Dễ tìm và sửa code
3. **Scalability**: Dễ thêm features mới
4. **Testability**: Có thể test từng layer
5. **Clean Code**: Code tổ chức rõ ràng, dễ đọc

## Troubleshooting

### Lỗi: ModuleNotFoundError: No module named 'app'
**Giải pháp**: Đảm bảo chạy từ thư mục root của project

### Lỗi: ImportError trong utils
**Giải pháp**: Kiểm tra file `app/utils/__init__.py` đã tồn tại

### Lỗi: Template not found
**Giải pháp**: Cập nhật `template_folder` trong Blueprint:
```python
Blueprint("name", __name__, template_folder="../views")
```

### Lỗi: Database connection
**Giải pháp**: Kiểm tra `DATABASE_URL` trong `.env` hoặc `app/config/settings.py`
