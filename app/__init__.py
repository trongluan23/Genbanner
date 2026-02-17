"""
Flask Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    from app.config.settings import Config
    app.config.from_object(Config)
    
    # Ensure required directories exist
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.OUTPUTS_FOLDER, exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Vui lòng đăng nhập để truy cập trang này."
    login_manager.login_message_category = "error"
    
    # Register blueprints
    from app.controllers.banner_controller import banner_bp
    from app.controllers.auth_controller import auth_bp
    
    app.register_blueprint(banner_bp)
    app.register_blueprint(auth_bp)
    
    # Create database tables
    with app.app_context():
        from app.models.user import User
        from app.models.banner import Banner
        db.create_all()
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        try:
            if user_id is None:
                return None
            uid = int(user_id)
        except (ValueError, TypeError):
            return None
        return User.query.get(uid)
    
    # Static file routes
    from flask import send_from_directory
    
    @app.route('/images/<path:filename>')
    def serve_image(filename):
        response = send_from_directory(Config.UPLOAD_FOLDER, filename)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    
    @app.route('/outputs/<path:filename>')
    def serve_output(filename):
        response = send_from_directory(Config.OUTPUTS_FOLDER, filename)
        response.headers['Cache-Control'] = 'public, max-age=3600'
        return response
    
    return app
