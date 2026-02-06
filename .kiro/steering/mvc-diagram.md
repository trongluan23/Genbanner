---
inclusion: auto
---

# MVC Architecture Diagram

## Cấu trúc tổng quan

```
┌─────────────────────────────────────────────────────────────┐
│                         USER REQUEST                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    🎮 CONTROLLER LAYER                       │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │ auth_controller.py   │  │ banner_controller.py │        │
│  │ - login()            │  │ - home()             │        │
│  │ - register()         │  │ - create()           │        │
│  │ - logout()           │  │ - history()          │        │
│  └──────────────────────┘  └──────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    💼 SERVICE LAYER                          │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │ banner_service.py    │  │ file_service.py      │        │
│  │ - create_banner()    │  │ - save_files()       │        │
│  │ - save_to_db()       │  │ - cleanup_files()    │        │
│  └──────────────────────┘  └──────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    🔧 UTILS LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ genbanner.py │  │ process      │  │ portrait.py  │     │
│  │              │→ │ background   │→ │ square.py    │     │
│  │              │  │ .py          │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                           ↓                                  │
│                  ┌──────────────────┐                       │
│                  │ openai_client.py │                       │
│                  │ (AI Processing)  │                       │
│                  └──────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    📊 MODEL LAYER                            │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │ user.py              │  │ banner.py            │        │
│  │ - User model         │  │ - Banner model       │        │
│  │ - Authentication     │  │ - Banner history     │        │
│  └──────────────────────┘  └──────────────────────┘        │
│                              ↓                               │
│                    ┌──────────────────┐                     │
│                    │    DATABASE      │                     │
│                    │  (PostgreSQL)    │                     │
│                    └──────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    🎨 VIEW LAYER                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ home.html│  │index.html│  │banner.html│ │history.html│ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                         USER RESPONSE                        │
└─────────────────────────────────────────────────────────────┘
```

## Chi tiết luồng xử lý

### 1. User tạo banner mới

```
POST /create
    ↓
banner_controller.create_post()
    ├─ Extract form data
    ├─ Get uploaded files
    ↓
FileService.save_uploaded_files()
    ├─ Validate files
    ├─ Save to user folder
    ├─ Return file paths
    ↓
BannerService.create_banner()
    ├─ Call genbanner()
    │   ├─ processbackground.preprocess()
    │   ├─ processbackground.resize()
    │   └─ portrait/square.generate()
    │       └─ OpenAI API call
    ├─ Save to database
    │   └─ Banner.create()
    └─ Return result
    ↓
render_template('banner.html')
    └─ Display generated banner
```

### 2. User xem lịch sử

```
GET /history
    ↓
banner_controller.history()
    ├─ Query banners by user_id
    ├─ Banner.query.filter_by()
    └─ Add image URLs
    ↓
render_template('history.html')
    └─ Display banner list
```

### 3. User đăng nhập

```
POST /auth/login
    ↓
auth_controller.login()
    ├─ Validate credentials
    ├─ User.query.filter_by(email)
    ├─ check_password_hash()
    └─ login_user()
    ↓
redirect to /create
```

## Dependency Flow

```
app.py
  └─ app/__init__.py (create_app)
      ├─ config/settings.py
      ├─ models/
      │   ├─ user.py
      │   └─ banner.py
      ├─ controllers/
      │   ├─ auth_controller.py
      │   │   └─ models.user
      │   └─ banner_controller.py
      │       ├─ models.banner
      │       ├─ services.banner_service
      │       └─ services.file_service
      ├─ services/
      │   ├─ banner_service.py
      │   │   ├─ models.banner
      │   │   └─ utils.genbanner
      │   └─ file_service.py
      └─ utils/
          ├─ genbanner.py
          │   ├─ processbackground
          │   ├─ portrait
          │   └─ square
          ├─ processbackground.py
          │   └─ openai_client
          ├─ portrait.py
          │   └─ openai_client
          ├─ square.py
          │   └─ openai_client
          └─ openai_client.py
```

## File Responsibilities

### Controllers (🎮)
- Handle HTTP requests/responses
- Validate input
- Call services
- Return views

### Services (💼)
- Business logic
- Orchestrate operations
- Call utils and models
- Transaction management

### Utils (🔧)
- Helper functions
- AI processing
- Image manipulation
- External API calls

### Models (📊)
- Database schema
- Data validation
- Relationships
- Queries

### Views (🎨)
- HTML templates
- User interface
- Display data
- Forms

## Benefits of This Architecture

1. **Single Responsibility**: Each component has one job
2. **Loose Coupling**: Components are independent
3. **High Cohesion**: Related code is grouped together
4. **Easy Testing**: Mock dependencies easily
5. **Maintainable**: Easy to find and fix bugs
6. **Scalable**: Easy to add new features
