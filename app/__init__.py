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
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "banner.login"
    
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
        images_dir = os.path.join(app.root_path, '..', 'images')
        response = send_from_directory(images_dir, filename)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    
    return app
