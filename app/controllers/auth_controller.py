"""
Authentication Controller
Handles user login, registration, and logout
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="../views")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for("banner.create"))
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email không tồn tại", "error")
            return render_template("login.html")

        if not check_password_hash(user.password, password):
            flash("Sai mật khẩu", "error")
            return render_template("login.html")

        login_user(user, remember=remember)
        flash("Đăng nhập thành công!", "success")
        return redirect(url_for("banner.create"))

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for("banner.create"))
    
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validation
        if not email or not username or not password:
            flash("Vui lòng điền đầy đủ thông tin", "error")
            return render_template("register.html")

        if password != confirm_password:
            flash("Mật khẩu xác nhận không khớp", "error")
            return render_template("register.html")

        if len(password) < 6:
            flash("Mật khẩu phải có ít nhất 6 ký tự", "error")
            return render_template("register.html")

        email_exist = User.query.filter_by(email=email).first()
        user_exist = User.query.filter_by(username=username).first()

        if email_exist:
            flash("Email đã được sử dụng", "error")
            return render_template("register.html")
        
        if user_exist:
            flash("Tên người dùng đã tồn tại", "error")
            return render_template("register.html")

        # Create new user
        new_user = User(
            email=email,
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user, remember=True)
        flash("Đăng ký thành công!", "success")
        return redirect(url_for("banner.create"))

    return render_template("register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    """User logout"""
    logout_user()
    flash("Đã đăng xuất", "success")
    return redirect(url_for("auth.login"))
