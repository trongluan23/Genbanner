# Hướng Dẫn Deploy Lên Render

## Bước 1: Chuẩn Bị Trước Khi Deploy

### 1.1. Kiểm tra các file cần thiết
Đảm bảo bạn có đầy đủ các file sau:
- ✅ `Procfile` - Đã có
- ✅ `requirements.txt` - Đã có
- ✅ `.env.example` - Đã có
- ✅ `.gitignore` - Đã có

### 1.2. Cập nhật file app.py (nếu cần)
File `app.py` hiện tại đã được cấu hình đúng với:
- Đọc biến môi trường từ `.env`
- Sử dụng PORT từ environment variable
- Host `0.0.0.0` để chấp nhận kết nối từ bên ngoài

### 1.3. Tạo tài khoản và chuẩn bị
1. Tạo tài khoản tại [render.com](https://render.com)
2. Kết nối với GitHub repository của bạn
3. Chuẩn bị OpenAI API key

## Bước 2: Push Code Lên GitHub

```bash
# Khởi tạo git (nếu chưa có)
git init

# Thêm tất cả file
git add .

# Commit
git commit -m "Prepare for Render deployment"

# Thêm remote repository
git remote add origin https://github.com/username/your-repo.git

# Push lên GitHub
git push -u origin main
```

## Bước 3: Tạo Web Service Trên Render

### 3.1. Tạo Web Service mới
1. Đăng nhập vào [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Chọn repository GitHub của bạn
4. Click **"Connect"**

### 3.2. Cấu hình Web Service

**Basic Settings:**
- **Name**: `banner-generator` (hoặc tên bạn muốn)
- **Region**: Chọn region gần bạn nhất
- **Branch**: `main` (hoặc branch bạn muốn deploy)
- **Root Directory**: để trống
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  gunicorn app:app
  ```

**Instance Type:**
- Chọn **Free** (hoặc Paid nếu cần hiệu năng cao hơn)

### 3.3. Cấu hình Environment Variables

Click **"Advanced"** → **"Add Environment Variable"** và thêm các biến sau:

| Key | Value | Ghi chú |
|-----|-------|---------|
| `SECRET_KEY` | `your-random-secret-key-here` | Tạo key ngẫu nhiên mạnh |
| `OPENAI_API_KEY` | `sk-...` | API key từ OpenAI |
| `PYTHON_VERSION` | `3.11.0` | Phiên bản Python |
| `PORT` | `10000` | Render tự động set, không cần thêm |

**Cách tạo SECRET_KEY mạnh:**
```python
import secrets
print(secrets.token_hex(32))
```

### 3.4. Cấu hình Auto-Deploy
- Bật **"Auto-Deploy"** để tự động deploy khi push code mới

## Bước 4: Deploy

1. Click **"Create Web Service"**
2. Render sẽ bắt đầu build và deploy
3. Theo dõi logs để kiểm tra quá trình deploy
4. Đợi 5-10 phút cho lần deploy đầu tiên

## Bước 5: Kiểm Tra Sau Khi Deploy

### 5.1. Kiểm tra logs
- Vào **"Logs"** tab để xem logs real-time
- Đảm bảo không có lỗi

### 5.2. Test ứng dụng
1. Mở URL được cung cấp: `https://your-app-name.onrender.com`
2. Test upload ảnh và tạo banner
3. Kiểm tra các chức năng chính

## Bước 6: Xử Lý Vấn Đề Thường Gặp

### 6.1. Lỗi "Application failed to respond"
**Nguyên nhân:** App không start đúng cách

**Giải pháp:**
1. Kiểm tra logs trong Render Dashboard
2. Đảm bảo `Procfile` có nội dung: `web: gunicorn app:app`
3. Kiểm tra file `app.py` có biến `app` được export

### 6.2. Lỗi "Module not found"
**Nguyên nhân:** Thiếu dependencies

**Giải pháp:**
1. Kiểm tra `requirements.txt` có đầy đủ packages
2. Rebuild service trong Render Dashboard

### 6.3. Lỗi OpenCV
**Nguyên nhân:** `opencv-python` không hoạt động trên môi trường serverless

**Giải pháp:**
- File `requirements.txt` đã sử dụng `opencv-python-headless==4.8.1.78` ✅
- Đây là phiên bản không cần GUI, phù hợp cho server

### 6.4. Lỗi Database
**Nguyên nhân:** SQLite không persistent trên Render Free tier

**Giải pháp:**
- Render Free tier có disk ephemeral (mất data khi restart)
- Nếu cần persistent database, nâng cấp lên Paid tier hoặc dùng PostgreSQL

### 6.5. Lỗi File Upload
**Nguyên nhân:** Disk không persistent

**Giải pháp:**
- Sử dụng cloud storage (AWS S3, Cloudinary) cho production
- Hoặc nâng cấp lên Paid tier với persistent disk

## Bước 7: Tối Ưu Hóa (Tùy Chọn)

### 7.1. Thêm Health Check
Thêm endpoint health check trong code:

```python
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

Cấu hình trong Render:
- **Health Check Path**: `/health`

### 7.2. Cấu hình Persistent Disk (Paid tier)
1. Vào **"Settings"** → **"Disks"**
2. Click **"Add Disk"**
3. Mount path: `/opt/render/project/src/images`
4. Size: 1GB trở lên

### 7.3. Sử dụng PostgreSQL thay vì SQLite
1. Tạo PostgreSQL database trong Render
2. Cập nhật `DATABASE_URL` trong Environment Variables
3. Sửa code để sử dụng PostgreSQL

## Bước 8: Monitoring và Maintenance

### 8.1. Theo dõi logs
- Vào **"Logs"** tab thường xuyên
- Set up email alerts cho errors

### 8.2. Kiểm tra metrics
- **"Metrics"** tab: CPU, Memory, Request count
- Free tier có giới hạn 750 hours/month

### 8.3. Backup
- Backup code trên GitHub
- Backup database nếu dùng PostgreSQL
- Backup uploaded images nếu dùng persistent disk

## Lưu Ý Quan Trọng

### Free Tier Limitations:
- ⚠️ Service sẽ sleep sau 15 phút không hoạt động
- ⚠️ Request đầu tiên sau khi sleep sẽ mất 30-60 giây để wake up
- ⚠️ Disk không persistent (mất data khi restart)
- ⚠️ 750 hours/month (đủ cho 1 service chạy 24/7)

### Khuyến Nghị:
- ✅ Sử dụng cloud storage cho uploaded images
- ✅ Sử dụng PostgreSQL cho database
- ✅ Nâng cấp lên Paid tier nếu cần production-ready
- ✅ Set up monitoring và alerts
- ✅ Thường xuyên kiểm tra logs

## Tài Nguyên Hữu Ích

- [Render Documentation](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/deploy-flask)
- [Render Free Tier Limits](https://render.com/docs/free)

## Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra logs trong Render Dashboard
2. Xem [Render Community](https://community.render.com)
3. Liên hệ Render Support (Paid tier)
