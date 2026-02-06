# 🎨 AI Banner Generator

Ứng dụng web tạo banner quảng cáo chuyên nghiệp sử dụng AI.

## ✨ Tính Năng

- 🤖 **AI-Powered**: Sử dụng OpenAI để xử lý và tối ưu hình ảnh
- 📐 **Nhiều Kích Thước**: Hỗ trợ 6 kích thước banner phổ biến
- 🎨 **Tùy Chỉnh**: Thêm logo, text, CTA, discount
- 💾 **Lưu Trữ**: Lịch sử banner được lưu trong database
- 🔐 **Bảo Mật**: Đăng ký/đăng nhập với mã hóa password
- 📱 **Responsive**: Giao diện đẹp trên mọi thiết bị

## 🚀 Cài Đặt Local

### Yêu Cầu
- Python 3.10+
- OpenAI API Key

### Các Bước

1. Clone repository:
```bash
git clone https://github.com/YOUR_USERNAME/ai-banner-generator.git
cd ai-banner-generator
```

2. Tạo virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

4. Tạo file `.env`:
```env
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
```

5. Chạy app:
```bash
python app.py
```

6. Truy cập: http://localhost:5000

## 📦 Deploy

Xem hướng dẫn chi tiết trong [DEPLOY.md](DEPLOY.md)

**Platforms hỗ trợ:**
- ✅ Render (Khuyến nghị)
- ✅ Railway
- ✅ PythonAnywhere
- ✅ Heroku

## 🛠️ Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **AI**: OpenAI API
- **Image Processing**: OpenCV, NumPy
- **Database**: SQLite (local), PostgreSQL (production)
- **Architecture**: MVC (Model-View-Controller) + Services

## 🏗️ Project Structure (MVC)

```
app/
├── models/          # Database models (User, Banner)
├── views/           # HTML templates
├── controllers/     # Route handlers (auth, banner)
├── services/        # Business logic (banner, file)
├── utils/           # AI processing utilities
└── config/          # Configuration
```

**📚 Documentation**: See [START_HERE.md](START_HERE.md) for complete MVC documentation

## ✅ Tests

```bash
python test_structure.py
```

**Status**: 6/6 tests passing ✅

## 📸 Screenshots

### Trang Tạo Banner
![Create Banner](screenshots/create.png)

### Lịch Sử Banner
![History](screenshots/history.png)

## 🤝 Contributing

Pull requests are welcome!

## 📄 License

MIT License

## 👤 Author

Your Name - [@yourhandle](https://twitter.com/yourhandle)
