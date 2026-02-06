"""
Banner Controller
Handles banner creation, viewing, and management
"""
import base64
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.banner import Banner
from app.services.banner_service import BannerService
from app.services.file_service import FileService

banner_bp = Blueprint("banner", __name__, template_folder="../views")

@banner_bp.route("/")
def home():
    """Home page"""
    return render_template("home.html")

@banner_bp.route("/create", methods=["GET"])
@login_required
def create():
    """Banner creation page"""
    return render_template("index.html", user=current_user)

@banner_bp.route("/create", methods=["POST"])
@login_required
def create_post():
    """Process banner creation"""
    # Extract form data
    form_data = {
        "size": request.form.get("size"),
        "company_name": request.form.get("company_name"),
        "product_name": request.form.get("product_name"),
        "subtext": request.form.get("subtexts"),
        "website": request.form.get("website"),
        "cta": request.form.get("call_to_action"),
        "discount": request.form.get("discount"),
        "phone": request.form.get("phone")
    }
    
    # Get uploaded files
    files = {
        "background": request.files.get("background"),
        "logo": request.files.get("logo"),
        "product": request.files.get("product")
    }
    
    # Save uploaded files
    file_service = FileService(current_user.id)
    file_paths = file_service.save_uploaded_files(files)
    
    # Merge file paths into form data
    form_data.update(file_paths)
    
    # Generate banner
    banner_service = BannerService()
    try:
        result = banner_service.create_banner(current_user.id, form_data, file_paths)
        
        if not result:
            flash("Không thể tạo banner. Vui lòng thử lại.", "error")
            return redirect(url_for("banner.create"))
        
        # Encode image for display
        image_data_uri = f"data:image/png;base64,{result['encoded_image']}"
        
        return render_template("banner.html",
                             generated_image=result['generated_path'],
                             image_data_uri=image_data_uri,
                             banner_id=result['banner_id'])
    
    except Exception as e:
        print(f"Error creating banner: {e}")
        flash("Lỗi khi tạo banner. Vui lòng thử lại.", "error")
        return redirect(url_for("banner.create"))

@banner_bp.route("/history")
@login_required
def history():
    """View user's banner history"""
    banners = Banner.query.filter_by(user_id=current_user.id)\
                          .order_by(Banner.date_created.desc())\
                          .all()
    
    # Add image URLs
    for banner in banners:
        banner.image_url = url_for('banner.get_banner_image', banner_id=banner.id)
    
    return render_template("history.html", banners=banners, user=current_user)

@banner_bp.route("/banner/<int:banner_id>")
@login_required
def view_banner(banner_id):
    """View a specific banner"""
    banner = Banner.query.get_or_404(banner_id)
    
    # Check ownership
    if banner.user_id != current_user.id:
        flash("Bạn không có quyền xem banner này", "error")
        return redirect(url_for("banner.create"))
    
    # Get image from database
    if banner.banner_image:
        encoded_string = base64.b64encode(banner.banner_image).decode("utf-8")
        image_data_uri = f"data:image/png;base64,{encoded_string}"
    else:
        image_data_uri = None
        flash("Không tìm thấy hình ảnh banner", "error")
    
    return render_template("banner.html",
                         generated_image=None,
                         image_data_uri=image_data_uri,
                         banner_id=banner.id,
                         banner=banner)

@banner_bp.route("/banner/<int:banner_id>/image")
@login_required
def get_banner_image(banner_id):
    """Serve banner image from database"""
    banner = Banner.query.get_or_404(banner_id)
    
    # Check ownership
    if banner.user_id != current_user.id:
        return "Unauthorized", 403
    
    if not banner.banner_image:
        return "Image not found", 404
    
    return Response(banner.banner_image, mimetype='image/png')

@banner_bp.route("/banner/<int:banner_id>/delete", methods=["POST"])
@login_required
def delete_banner(banner_id):
    """Delete a banner"""
    banner = Banner.query.get_or_404(banner_id)
    
    # Check ownership
    if banner.user_id != current_user.id:
        flash("Bạn không có quyền xóa banner này", "error")
        return redirect(url_for("banner.history"))
    
    try:
        # Delete from database
        db.session.delete(banner)
        db.session.commit()
        flash("Đã xóa banner thành công", "success")
        
        # Clean up physical files
        file_service = FileService(current_user.id)
        file_service.cleanup_banner_files(banner)
        
    except Exception as e:
        print(f"Error deleting banner: {e}")
        db.session.rollback()
        flash("Lỗi khi xóa banner", "error")
    
    return redirect(url_for("banner.history"))
