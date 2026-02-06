# Project Structure

## Root Directory
- `app.py`: Main application entry point, runs Flask development server
- `*.png`: Generated preprocessed background images (temporary files)
- `banner_*.png`: Generated banner output files

## Core Application (`website/`)
- `__init__.py`: Flask app factory, database initialization, login manager setup
- `auth.py`: Main blueprint with routes for banner generation (authentication routes commented out)
- `models.py`: SQLAlchemy User model definition
- `.env`: Environment configuration file

## Templates (`website/template/`)
- `index.html`: Main banner creation form interface
- `banner.html`: Display generated banner results
- `login.html`, `register.html`, `edit.html`: Authentication templates (currently unused)

## Utilities (`untils/`) 
**Note**: Directory name contains typo - should be "utils"
- `genbanner.py`: Main banner generation orchestrator
- `processbackground.py`: AI background processing and resizing logic
- `square.py`: Banner composition and text overlay (referenced but not examined)
- `banner_poitrait.py`: Portrait banner generation (referenced but not examined)
- `until.py`: OpenAI client configuration (typo - should be "util.py")

## Assets
- `images/`: User uploaded and sample images (background, logo, product)
- `instance/`: SQLite database storage
- `outputs/`: Generated banner components and final outputs

## File Naming Conventions
- Uploaded files are saved with generic names: `background.*`, `logo.*`, `product.*`
- Generated files use descriptive prefixes: `preprocessed_background`, `bg_square`, `bg_landscape_*`, `bg_portrait_*`
- Output banners saved to `images/banner_square.png`

## Data Flow
1. User uploads images and form data via `index.html`
2. `auth.py` processes uploads, saves to `images/` directory
3. `genbanner.py` orchestrates the generation pipeline
4. `processbackground.py` enhances backgrounds using OpenAI API
5. Final banner saved and displayed via `banner.html`

## Security Notes
- File uploads use `secure_filename()` for safety
- Images served through custom route `/images/<filename>`
- Authentication system exists but is currently disabled