"""
Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Get base directory (project root)
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    SECRET_KEY = os.environ.get("SECRET_KEY", "hi")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:Luan23102003#@localhost/genbanner"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "images")
    OUTPUTS_FOLDER = os.path.join(BASE_DIR, "outputs")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Default config
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
