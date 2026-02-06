# Hướng Dẫn Khắc Phục Lỗi

## Lỗi: Không Hiển Thị Ảnh Trong History

### Bước 1: Kiểm tra Database

Chạy script kiểm tra database:

```bash
python check_db.py
```

Script này sẽ hiển thị:
- Số lượng users và banners trong database
- Kích thước của banner_image (binary data)
- Các đường dẫn file

**Kết quả mong đợi:**
```
✅ Banner Image: 123456 bytes
```

**Nếu thấy:**
```
❌ Banner Image: None
```

Có nghĩa là ảnh chưa được lưu vào database. Hãy tạo banner mới để test.

### Bước 2: Kiểm tra Browser Console

1. Mở trang History trong trình duyệt
2. Nhấn F12 để mở Developer Tools
3. Chuyển sang tab Console
4. Xem các log messages:

```javascript
Total banner images: 3
Image 1: http://localhost:5000/banner/1/image
✅ Image 1 loaded successfully
```

**Nếu thấy lỗi 404:**
```
❌ Image 1 failed to load: http://localhost:5000/banner/1/image
GET http://localhost:5000/banner/1/image 404 (Not Found)
```

Có nghĩa là route không hoạt động đúng.

**Nếu thấy lỗi 403:**
```
❌ Image 1 failed to load: http://localhost:5000/banner/1/image
GET http://localhost:5000/banner/1/image 403 (Forbidden)
```

Có nghĩa là bạn không có quyền xem ảnh (không phải owner).

### Bước 3: Test Route Trực Tiếp

Mở trình duyệt và truy cập trực tiếp:
```
http://localhost:5000/banner/1/image
```

Thay `1` bằng ID banner thực tế từ database.

**Kết quả mong đợi:** Ảnh banner hiển thị

**Nếu thấy lỗi:** Kiểm tra terminal/console logs

### Bước 4: Kiểm tra Terminal Logs

Khi truy cập trang History, terminal sẽ hiển thị:

```
Requesting image for banner ID: 1
Banner found: 1, User: 1, Current user: 1
Serving image, size: 123456 bytes
127.0.0.1 - - [17/Jan/2026 10:30:45] "GET /banner/1/image HTTP/1.1" 200 -
```

**Nếu không thấy log nào:** Route không được gọi, kiểm tra URL trong template

**Nếu thấy "Banner image is None":** Database không có ảnh, tạo banner mới

### Bước 5: Xóa Database Cũ và Tạo Mới

Nếu database bị lỗi cấu trúc (do thay đổi model):

```bash
# Backup database cũ
cp instance/database.db instance/database_backup.db

# Xóa database cũ
rm instance/database.db

# Tạo database mới
python -c "from website import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database created!')"
```

Sau đó:
1. Đăng ký tài khoản mới
2. Tạo banner mới
3. Kiểm tra History

### Bước 6: Kiểm tra Quyền File

```bash
# Kiểm tra quyền thư mục instance
ls -la instance/

# Nếu cần, cấp quyền
chmod 755 instance/
chmod 644 instance/database.db
```

## Lỗi: Upload File Thất Bại

### Kiểm tra kích thước file

Mặc định Flask giới hạn upload 16MB. Để tăng:

```python
# Trong website/__init__.py
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

### Kiểm tra thư mục images

```bash
# Tạo thư mục nếu chưa có
mkdir -p images/user_1

# Cấp quyền
chmod -R 755 images/
```

## Lỗi: OpenAI API

### Lỗi: "Invalid API Key"

Kiểm tra file `untils/until.py`:

```python
client = OpenAI(api_key="your-api-key-here")
```

Thay bằng API key thực tế từ https://platform.openai.com/api-keys

### Lỗi: "Rate limit exceeded"

Bạn đã vượt quá giới hạn API. Đợi vài phút hoặc nâng cấp plan.

### Lỗi: "Insufficient credits"

Tài khoản OpenAI hết credits. Nạp thêm tiền tại https://platform.openai.com/account/billing

## Lỗi: Database Locked

```
sqlite3.OperationalError: database is locked
```

**Giải pháp:**

1. Đóng tất cả kết nối đến database
2. Restart Flask app
3. Nếu vẫn lỗi, chuyển sang PostgreSQL (xem DEPLOY_VPS.md)

## Lỗi: Import Error

```
ModuleNotFoundError: No module named 'flask'
```

**Giải pháp:**

```bash
# Kích hoạt virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Cài lại dependencies
pip install -r requirements.txt
```

## Lỗi: Port Already in Use

```
OSError: [Errno 48] Address already in use
```

**Giải pháp:**

```bash
# Tìm process đang dùng port 5000
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows

# Hoặc dùng port khác
python app.py --port 5001
```

## Lỗi: Template Not Found

```
jinja2.exceptions.TemplateNotFound: index.html
```

**Giải pháp:**

Kiểm tra cấu trúc thư mục:
```
website/
  template/
    index.html
    banner.html
    history.html
    login.html
    register.html
```

Đảm bảo thư mục tên là `template` (không có 's').

## Lỗi: CSS/JS Không Load

### Kiểm tra đường dẫn

Trong template, dùng CDN:
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
```

### Kiểm tra Internet

Nếu không có internet, download Bootstrap và lưu local:
```
website/
  static/
    css/
      bootstrap.min.css
    js/
      bootstrap.bundle.min.js
```

Và thay đổi trong template:
```html
<link href="{{ url_for('static', filename='css/bootstrap.min.css') }}" rel="stylesheet">
```

## Lỗi: Login Không Hoạt Động

### Kiểm tra SECRET_KEY

```python
# Trong website/__init__.py
app.config["SECRET_KEY"] = "hi"  # ❌ Quá đơn giản

# Nên dùng:
import secrets
app.config["SECRET_KEY"] = secrets.token_hex(32)
```

### Kiểm tra session

Xóa cookies và thử lại:
1. Mở Developer Tools (F12)
2. Tab Application > Cookies
3. Xóa tất cả cookies
4. Refresh trang

## Cần Thêm Trợ Giúp?

1. Kiểm tra terminal logs khi chạy app
2. Kiểm tra browser console (F12)
3. Chạy `python check_db.py` để kiểm tra database
4. Đọc file logs trong `/var/log/banner-generator/` (nếu deploy lên VPS)

## Debug Mode

Để bật debug mode chi tiết:

```python
# Trong app.py
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
```

**Lưu ý:** KHÔNG bật debug mode trên production server!
