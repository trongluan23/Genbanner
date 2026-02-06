---
inclusion: auto
---

# Project Structure - MVC Architecture

## Root Directory
- `app.py`: Main application entry point, runs Flask development server
- `*.png`: Generated preprocessed background images (temporary files)
- `banner_*.png`: Generated banner output files

## Core Application (`app/`)
Organized following MVC (Model-View-Controller) pattern:

### Models (`app/models/`)
Database models using SQLAlchemy ORM:
- `user.py`: User model with authentication
- `banner.py`: Banner generation history model

### Views (`app/views/`)
HTML templates for user interface:
- `base.html`: Base template with common layout
- `home.html`: Landing page
- `index.html`: Main banner creation form interface
- `banner.html`: Display generated banner results
- `history.html`: User's banner history
- `login.html`, `register.html`: Authentication templates

### Controllers (`app/controllers/`)
Request handlers and route definitions:
- `auth_controller.py`: Authentication routes (login, register, logout)
- `banner_controller.py`: Banner CRUD operations (create, view, delete, history)

### Services (`app/services/`)
Business logic layer:
- `banner_service.py`: Banner generation orchestration and database operations
- `file_service.py`: File upload and management logic

### Utils (`app/utils/`)
Utility functions and AI processing:
- `genbanner.py`: Main banner generation orchestrator
- `processbackground.py`: AI background processing and resizing logic
- `square.py`: Square banner composition and text overlay
- `portrait.py`: Portrait banner generation
- `openai_client.py`: OpenAI API client configuration

### Config (`app/config/`)
Application configuration:
- `settings.py`: Database, secret key, upload settings

## Assets
- `images/`: User uploaded and sample images (background, logo, product)
- `instance/`: Database storage
- `outputs/`: Generated banner components and final outputs

## File Naming Conventions
- Uploaded files: `{type}_{timestamp}.{ext}` in `images/user_{id}/`
- Generated files: `preprocessed_background{size}.png`, `bg_square{size}.png`, etc.
- Output banners: `banner_{type}_{uuid}.png` in `outputs/`

## Data Flow (MVC Pattern)
1. User request → **Controller** (auth_controller.py or banner_controller.py)
2. Controller → **Service** (banner_service.py, file_service.py)
3. Service → **Utils** (genbanner.py → processbackground.py → portrait/square.py)
4. Service → **Model** (save to database via User/Banner models)
5. Controller → **View** (render template with data)

## Example: Banner Creation Flow
```
POST /create
    ↓
banner_controller.create_post()        # Controller
    ↓
FileService.save_uploaded_files()      # Service - File handling
    ↓
BannerService.create_banner()          # Service - Business logic
    ↓
genbanner() → processbackground()      # Utils - AI processing
    ↓
Banner.save()                          # Model - Database
    ↓
render_template('banner.html')         # View - Display
```

## Security Notes
- File uploads use `secure_filename()` for safety
- Images served through custom route `/images/<filename>`
- User authentication with Flask-Login
- Password hashing with werkzeug.security
- CSRF protection enabled
- User-specific folders for uploaded files

## Blueprint Structure
- `auth_bp`: `/auth/*` - Authentication routes
- `banner_bp`: `/*` - Banner operations (home, create, history, view, delete)
