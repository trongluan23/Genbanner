# ⚡ Quick Start - Deploy trong 10 phút

## 🎯 Cách Nhanh Nhất: Deploy lên Render

### 1️⃣ Push Code lên GitHub (2 phút)

```bash
# Trong thư mục project
git init
git add .
git commit -m "Initial commit"

# Tạo repo mới trên GitHub, sau đó:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2️⃣ Deploy trên Render (5 phút)

1. Vào https://render.com → Sign up (dùng GitHub)
2. Click **"New +"** → **"Web Service"**
3. Connect repo GitHub vừa tạo
4. Điền thông tin:
   - **Name**: `ai-banner-generator`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: **Free**

5. Click **"Advanced"** → Add Environment Variables:
   ```
   SECRET_KEY = abc123xyz789  (tạo random string)
   OPENAI_API_KEY = sk-...    (lấy từ OpenAI)
   ```

6. Click **"Create Web Service"**

### 3️⃣ Đợi Deploy (3 phút)

- Render sẽ tự động build và deploy
- Xem logs để theo dõi tiến trình
- Khi thấy "Starting gunicorn" → Thành công!

### 4️⃣ Truy Cập Website

URL: `https://ai-banner-generator.onrender.com`

---

## 🔑 Lấy OpenAI API Key

1. Vào https://platform.openai.com
2. Đăng ký/Đăng nhập
3. Vào **API Keys** → **Create new secret key**
4. Copy key (chỉ hiện 1 lần!)
5. Nạp credit vào account (tối thiểu $5)

---

## ⚠️ Lưu Ý

- **Free tier của Render**: App sẽ sleep sau 15 phút không dùng
- **Lần đầu truy cập**: Có thể mất 30-60s để wake up
- **Database**: SQLite sẽ reset khi deploy mới → Nên dùng PostgreSQL

### Thêm PostgreSQL (Optional - Khuyến nghị)

1. Trong Render dashboard → **"New +"** → **"PostgreSQL"**
2. Tạo database (Free tier)
3. Copy **Internal Database URL**
4. Add vào Environment Variables:
   ```
   DATABASE_URL = postgresql://...
   ```
5. Redeploy web service

---

## 🎉 Xong!

Website của bạn đã online tại: `https://YOUR-APP-NAME.onrender.com`

Share link này với bạn bè để test!
