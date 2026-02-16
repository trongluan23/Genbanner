# Hướng dẫn Deploy lên Render

## Các bước chuẩn bị

### 1. Kiểm tra Environment Variables trên Render

Đảm bảo bạn đã cấu hình các biến môi trường sau trong Render Dashboard:

```
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=postgresql://... (Render tự động tạo nếu bạn dùng PostgreSQL)
```

### 2. Kiểm tra Procfile

File `Procfile` phải có nội dung:
```
web: gunicorn app:app
```

### 3. Kiểm tra requirements.txt

Đảm bảo tất cả dependencies đã được liệt kê trong `requirements.txt`:
- Flask
- Flask-SQLAlchemy
- Flask-Login
- opencv-python-headless (quan trọng: phải dùng headless cho server)
- numpy
- openai
- python-dotenv
- psycopg2-binary (cho PostgreSQL)
- gunicorn

## Các vấn đề thường gặp và cách khắc phục

### Lỗi: "Lỗi khi tạo banner. Vui lòng thử lại."

**Nguyên nhân:**
1. OPENAI_API_KEY không được cấu hình hoặc không hợp lệ
2. Thư mục `outputs/` không tồn tại hoặc không có quyền ghi
3. File upload không được lưu đúng đường dẫn
4. OpenAI API rate limit hoặc lỗi kết nối

**Cách khắc phục:**
1. Kiểm tra logs trên Render Dashboard để xem lỗi cụ thể
2. Đảm bảo OPENAI_API_KEY đã được set trong Environment Variables
3. Code đã được cập nhật để tự động tạo thư mục `outputs/` và `images/`
4. Kiểm tra quota OpenAI API của bạn

### Lỗi: File không tìm thấy

**Nguyên nhân:**
- Đường dẫn file hardcoded không tồn tại trên server

**Cách khắc phục:**
- Code đã được sửa để dùng đường dẫn động từ file upload thực tế
- Không còn dùng hardcoded paths như `"images/background.jpg"`

### Lỗi: OpenCV không hoạt động

**Nguyên nhân:**
- Dùng `opencv-python` thay vì `opencv-python-headless`

**Cách khắc phục:**
- Đảm bảo `requirements.txt` dùng `opencv-python-headless==4.8.1.78`

## Xem logs để debug

Trên Render Dashboard:
1. Vào service của bạn
2. Click tab "Logs"
3. Xem real-time logs khi tạo banner
4. Tìm các dòng bắt đầu bằng "Error" hoặc "Traceback"

## Test local trước khi deploy

```bash
# Set environment variables
set OPENAI_API_KEY=your-key-here
set SECRET_KEY=test-secret-key

# Run locally
python app.py
```

## Checklist trước khi deploy

- [ ] OPENAI_API_KEY đã được set trong Render Environment Variables
- [ ] SECRET_KEY đã được set (không dùng "hi" trong production)
- [ ] requirements.txt có opencv-python-headless
- [ ] Procfile đúng format
- [ ] Code đã commit và push lên Git repository
- [ ] Render service đã được connect với Git repo

## Monitoring sau khi deploy

1. Test tạo banner với các size khác nhau
2. Kiểm tra logs nếu có lỗi
3. Verify OpenAI API calls đang hoạt động
4. Kiểm tra database có lưu banner không
