# Debug OpenAI File Reading Issue on Server

## Vấn đề đã sửa

### 1. File handle không được đóng đúng cách
**Trước:**
```python
result = client.images.edit(
    image=open(background_path, "rb"),  # File không được đóng
    ...
)
```

**Sau:**
```python
with open(background_path, "rb") as image_file:
    result = client.images.edit(
        image=image_file,  # File sẽ tự động đóng
        ...
    )
```

### 2. Thêm kiểm tra file tồn tại và quyền truy cập
- Kiểm tra file có tồn tại không với `os.path.isfile()`
- Kiểm tra kích thước file với `os.path.getsize()`
- Set quyền file 644 khi lưu (readable by all)
- Set quyền thư mục 755 cho outputs folder

### 3. Thêm logging chi tiết
- Log file size khi đọc
- Log đường dẫn đầy đủ
- Log lỗi chi tiết với traceback

## Cách kiểm tra trên server

### 1. Kiểm tra quyền truy cập thư mục
```bash
ls -la images/user_1/
ls -la outputs/
```

Đảm bảo:
- Thư mục có quyền 755 (drwxr-xr-x)
- File có quyền 644 (-rw-r--r--)

### 2. Kiểm tra user chạy ứng dụng
```bash
whoami
ps aux | grep python
```

Đảm bảo user có quyền đọc/ghi vào thư mục images và outputs.

### 3. Kiểm tra logs
Xem logs của ứng dụng để tìm:
- "File saved: ..." - Xác nhận file được lưu
- "Background file size: ..." - Xác nhận file có thể đọc
- "Error generating background: ..." - Lỗi cụ thể

### 4. Kiểm tra biến môi trường
```bash
echo $OPENAI_API_KEY
```

Đảm bảo API key được set đúng trên server.

### 5. Test thủ công trên server
```python
import os
from openai import OpenAI

# Test đọc file
test_file = "images/user_1/logo_xxxxx.png"
print(f"File exists: {os.path.exists(test_file)}")
print(f"File size: {os.path.getsize(test_file)}")

# Test OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
with open(test_file, "rb") as f:
    result = client.images.edit(
        model="gpt-image-1",
        image=f,
        prompt="test",
        size="1024x1024"
    )
    print("Success!")
```

## Các vấn đề thường gặp trên server

### 1. SELinux (trên CentOS/RHEL)
```bash
# Kiểm tra SELinux
getenforce

# Tạm thời tắt để test
sudo setenforce 0

# Nếu đó là vấn đề, cấu hình đúng:
sudo chcon -R -t httpd_sys_rw_content_t images/
sudo chcon -R -t httpd_sys_rw_content_t outputs/
```

### 2. Đường dẫn tương đối vs tuyệt đối
Đảm bảo sử dụng đường dẫn tuyệt đối:
```python
# Trong settings.py
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "images")
```

### 3. Disk space
```bash
df -h
```

Đảm bảo còn đủ dung lượng để lưu file.

### 4. File system read-only
```bash
mount | grep "ro,"
```

Đảm bảo file system không ở chế độ read-only.

## Nếu vẫn không hoạt động

1. Thêm debug logging vào `app/utils/processbackground.py`:
```python
import sys
print(f"Python version: {sys.version}", file=sys.stderr)
print(f"Current working directory: {os.getcwd()}", file=sys.stderr)
print(f"File absolute path: {os.path.abspath(background_path)}", file=sys.stderr)
```

2. Kiểm tra OpenAI API có hoạt động không:
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

3. Kiểm tra network từ server có thể kết nối OpenAI không:
```bash
ping api.openai.com
curl -I https://api.openai.com
```
