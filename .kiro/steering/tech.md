# Technology Stack

## Backend Framework
- **Flask**: Python web framework with SQLAlchemy ORM
- **Flask-Login**: User authentication and session management
- **SQLite**: Database for user management (stored in `instance/database.db`)

## AI/Image Processing
- **OpenAI API**: GPT image editing model for background generation and enhancement
- **OpenCV (cv2)**: Image processing, resizing, and manipulation
- **NumPy**: Array operations for image data

## Frontend
- **HTML/CSS**: Simple form-based interface
- **Vanilla JavaScript**: File uploads and form handling (currently commented out)

## File Handling
- **Werkzeug**: Secure filename handling for uploads
- **Base64**: Image data encoding/decoding

## Project Structure
- Flask app factory pattern in `website/__init__.py`
- Blueprint-based routing in `website/auth.py`
- Utility modules in `untils/` directory (note: typo in folder name)

## Common Commands

### Development
```bash
python app.py
```
Runs the Flask development server with debug mode enabled.

### Database
The SQLite database is automatically created on first run. No manual setup required.

### Dependencies
Key imports suggest these packages are required:
- flask
- flask-sqlalchemy
- flask-login
- opencv-python
- numpy
- openai
- werkzeug

## Configuration Notes
- OpenAI API key is hardcoded in `untils/until.py` (should be moved to environment variables)
- Debug mode is enabled in production code
- Secret key is hardcoded as "hi" (should use secure random key)