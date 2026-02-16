"""
Banner Service
Business logic for banner generation and management
"""
import os
import base64
from app import db
from app.models.banner import Banner
from app.utils.genbanner import genbanner

class BannerService:
    """Service for banner operations"""
    
    def create_banner(self, user_id, form_data, file_paths):
        """
        Create a new banner
        
        Args:
            user_id: User ID
            form_data: Form data dictionary
            file_paths: Dictionary of file paths
            
        Returns:
            Dictionary with banner_id, generated_path, and encoded_image
        """
        try:
            print(f"Creating banner for user {user_id}")
            print(f"Form data: {form_data}")
            print(f"File paths: {file_paths}")
            
            # Generate banner using utility
            generated_path = genbanner(form_data)
            
            if not generated_path:
                print("Banner generation returned None")
                return None
                
            if not os.path.exists(generated_path):
                print(f"Generated banner file not found: {generated_path}")
                return None
            
            print(f"Banner generated at: {generated_path}")
            
            # Save to database
            banner_id = self._save_to_database(user_id, form_data, file_paths, generated_path)
            
            if not banner_id:
                print("Failed to save banner to database")
                return None
            
            # Encode image
            with open(generated_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            
            return {
                'banner_id': banner_id,
                'generated_path': generated_path,
                'encoded_image': encoded_string
            }
            
        except Exception as e:
            print(f"Error in create_banner: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _save_to_database(self, user_id, form_data, file_paths, generated_path):
        """Save banner to database"""
        try:
            # Read generated banner
            with open(generated_path, "rb") as f:
                banner_binary = f.read()
            
            # Read input images
            bg_binary = self._read_file(file_paths.get('background'))
            logo_binary = self._read_file(file_paths.get('logo'))
            prod_binary = self._read_file(file_paths.get('product'))
            
            # Create banner record
            new_banner = Banner(
                user_id=user_id,
                size=form_data.get('size'),
                company_name=form_data.get('company_name'),
                product_name=form_data.get('product_name'),
                subtext=form_data.get('subtext'),
                website=form_data.get('website'),
                call_to_action=form_data.get('cta'),
                discount=form_data.get('discount'),
                phone=form_data.get('phone'),
                banner_image=banner_binary,
                background_image=bg_binary,
                logo_image=logo_binary,
                product_image=prod_binary,
                background_path=file_paths.get('background'),
                logo_path=file_paths.get('logo'),
                product_path=file_paths.get('product'),
                generated_banner_path=generated_path
            )
            
            db.session.add(new_banner)
            db.session.commit()
            
            return new_banner.id
            
        except Exception as e:
            print(f"Error saving banner to database: {e}")
            db.session.rollback()
            return None
    
    def _read_file(self, file_path):
        """Read file as binary"""
        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as f:
                return f.read()
        return None
