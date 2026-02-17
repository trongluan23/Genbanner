"""
File Service
Handles file upload and management
"""
import os
import time
from werkzeug.utils import secure_filename

class FileService:
    """Service for file operations"""
    
    def __init__(self, user_id):
        from app.config.settings import Config
        self.user_id = user_id
        # Ensure base images directory exists
        base_images_dir = Config.UPLOAD_FOLDER
        os.makedirs(base_images_dir, exist_ok=True)
        
        self.user_folder = os.path.join(base_images_dir, f"user_{user_id}")
        os.makedirs(self.user_folder, exist_ok=True)
        print(f"User folder created/verified: {self.user_folder}")
    
    def save_uploaded_files(self, files):
        """
        Save uploaded files
        
        Args:
            files: Dictionary of file objects {name: file_obj}
            
        Returns:
            Dictionary of file paths
        """
        file_paths = {}
        
        try:
            if files.get('background'):
                file_paths['background'] = self._save_file(files['background'], 'background')
                print(f"Background saved: {file_paths.get('background')}")
            
            if files.get('logo'):
                file_paths['logo'] = self._save_file(files['logo'], 'logo')
                print(f"Logo saved: {file_paths.get('logo')}")
            
            if files.get('product'):
                file_paths['product'] = self._save_file(files['product'], 'product')
                print(f"Product saved: {file_paths.get('product')}")
        
        except Exception as e:
            print(f"Error saving uploaded files: {e}")
            import traceback
            traceback.print_exc()
        
        return file_paths
    
    def _save_file(self, file_obj, name_prefix):
        """Save a single file with timestamp"""
        if not file_obj:
            return None
        
        try:
            filename = secure_filename(file_obj.filename)
            _, ext = os.path.splitext(filename)
            timestamp = int(time.time())
            out_name = f"{name_prefix}_{timestamp}{ext or '.jpg'}"
            out_path = os.path.join(self.user_folder, out_name)
            file_obj.save(out_path)
            print(f"File saved: {out_path}")
            
            return out_path
        except Exception as e:
            print(f"Error saving file {name_prefix}: {e}")
            return None
    
    def cleanup_banner_files(self, banner):
        """Clean up physical files for a banner"""
        try:
            if banner.generated_banner_path and os.path.exists(banner.generated_banner_path):
                os.remove(banner.generated_banner_path)
            if banner.background_path and os.path.exists(banner.background_path):
                os.remove(banner.background_path)
            if banner.logo_path and os.path.exists(banner.logo_path):
                os.remove(banner.logo_path)
            if banner.product_path and os.path.exists(banner.product_path):
                os.remove(banner.product_path)
        except Exception as e:
            print(f"Error cleaning up files: {e}")
