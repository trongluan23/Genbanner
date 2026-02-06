# Quick Reference - MVC Structure

## 🚀 Cheat Sheet cho Developers

### Thêm Model mới

```python
# app/models/new_model.py
from app import db
from sqlalchemy.sql import func

class NewModel(db.Model):
    __tablename__ = 'new_model'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    
    def __repr__(self):
        return f'<NewModel {self.name}>'
```

```python
# app/models/__init__.py
from app.models.user import User
from app.models.banner import Banner
from app.models.new_model import NewModel  # Add this

__all__ = ['User', 'Banner', 'NewModel']
```

---

### Thêm Controller mới

```python
# app/controllers/new_controller.py
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app import db
from app.models.new_model import NewModel

new_bp = Blueprint("new", __name__, url_prefix="/new", template_folder="../views")

@new_bp.route("/")
@login_required
def index():
    items = NewModel.query.all()
    return render_template("new/index.html", items=items)

@new_bp.route("/create", methods=["POST"])
@login_required
def create():
    name = request.form.get("name")
    new_item = NewModel(name=name)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for("new.index"))
```

```python
# app/__init__.py - Register blueprint
from app.controllers.new_controller import new_bp
app.register_blueprint(new_bp)
```

---

### Thêm Service mới

```python
# app/services/new_service.py
from app import db
from app.models.new_model import NewModel

class NewService:
    """Service for new feature operations"""
    
    def create_item(self, data):
        """Create a new item"""
        try:
            new_item = NewModel(name=data['name'])
            db.session.add(new_item)
            db.session.commit()
            return new_item
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return None
    
    def get_all_items(self):
        """Get all items"""
        return NewModel.query.all()
```

```python
# app/controllers/new_controller.py - Use service
from app.services.new_service import NewService

@new_bp.route("/create", methods=["POST"])
@login_required
def create():
    service = NewService()
    result = service.create_item(request.form)
    if result:
        flash("Created successfully!", "success")
    else:
        flash("Error creating item", "error")
    return redirect(url_for("new.index"))
```

---

### Thêm Utility function

```python
# app/utils/new_util.py
def process_data(data):
    """Process data in some way"""
    # Your logic here
    return processed_data
```

```python
# Use in service
from app.utils.new_util import process_data

class NewService:
    def create_item(self, data):
        processed = process_data(data)
        # Continue...
```

---

### Thêm Template mới

```html
<!-- app/views/new/index.html -->
{% extends "base.html" %}

{% block title %}New Feature{% endblock %}

{% block content %}
<div class="container">
    <h1>New Feature</h1>
    
    {% for item in items %}
        <div class="item">{{ item.name }}</div>
    {% endfor %}
</div>
{% endblock %}
```

---

### Common Patterns

#### 1. Query Database
```python
# Get all
items = Model.query.all()

# Get by ID
item = Model.query.get(id)
item = Model.query.get_or_404(id)

# Filter
items = Model.query.filter_by(user_id=user_id).all()

# Order
items = Model.query.order_by(Model.date_created.desc()).all()

# Pagination
items = Model.query.paginate(page=1, per_page=10)
```

#### 2. Save to Database
```python
# Create
new_item = Model(name="test")
db.session.add(new_item)
db.session.commit()

# Update
item = Model.query.get(id)
item.name = "updated"
db.session.commit()

# Delete
item = Model.query.get(id)
db.session.delete(item)
db.session.commit()

# Rollback on error
try:
    db.session.commit()
except:
    db.session.rollback()
```

#### 3. Flash Messages
```python
from flask import flash

flash("Success message", "success")
flash("Error message", "error")
flash("Warning message", "warning")
flash("Info message", "info")
```

#### 4. Redirects
```python
from flask import redirect, url_for

return redirect(url_for('blueprint.route_name'))
return redirect(url_for('banner.home'))
return redirect(url_for('auth.login'))
```

#### 5. Authentication
```python
from flask_login import login_required, current_user

@route.route("/protected")
@login_required
def protected():
    user = current_user
    return render_template("page.html", user=user)
```

---

### File Locations Quick Reference

| What | Where |
|------|-------|
| Database models | `app/models/` |
| HTML templates | `app/views/` |
| Route handlers | `app/controllers/` |
| Business logic | `app/services/` |
| Helper functions | `app/utils/` |
| Configuration | `app/config/` |
| Static files | `static/` |
| Uploaded images | `images/` |
| Generated banners | `outputs/` |
| Database | `instance/` |

---

### Import Patterns

```python
# Models
from app.models.user import User
from app.models.banner import Banner

# Controllers
from app.controllers.auth_controller import auth_bp
from app.controllers.banner_controller import banner_bp

# Services
from app.services.banner_service import BannerService
from app.services.file_service import FileService

# Utils
from app.utils.genbanner import genbanner
from app.utils.openai_client import client

# Config
from app.config.settings import Config

# Database
from app import db

# Flask
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
```

---

### URL Patterns

```python
# Home
url_for('banner.home')              # /

# Banner operations
url_for('banner.create')            # /create
url_for('banner.history')           # /history
url_for('banner.view_banner', banner_id=1)  # /banner/1
url_for('banner.delete_banner', banner_id=1)  # /banner/1/delete

# Authentication
url_for('auth.login')               # /auth/login
url_for('auth.register')            # /auth/register
url_for('auth.logout')              # /auth/logout

# Static files
url_for('static', filename='style.css')
url_for('serve_image', filename='logo.png')
```

---

### Testing

```python
# Run all tests
python test_structure.py

# Test specific component
python -c "from app.models.user import User; print('OK')"
python -c "from app import create_app; app = create_app(); print('OK')"
```

---

### Common Commands

```bash
# Run development server
python app.py

# Create database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Drop database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.drop_all()"

# Python shell with app context
python
>>> from app import create_app, db
>>> app = create_app()
>>> app.app_context().push()
>>> from app.models.user import User
>>> User.query.all()
```

---

### Debugging

```python
# Print debug info
print(f"Debug: {variable}")
import traceback; traceback.print_exc()

# Flask debug mode
app.run(debug=True)

# Check current user
print(f"Current user: {current_user.username if current_user.is_authenticated else 'Anonymous'}")

# Check request data
print(f"Form data: {request.form}")
print(f"Files: {request.files}")
print(f"Method: {request.method}")
```

---

### Best Practices

1. **Controllers**: Chỉ xử lý HTTP, gọi services
2. **Services**: Chứa business logic, gọi models và utils
3. **Models**: Chỉ định nghĩa schema và relationships
4. **Utils**: Pure functions, không có side effects
5. **Always**: Rollback database on error
6. **Always**: Validate user input
7. **Always**: Check authentication/authorization
8. **Never**: Put business logic in controllers
9. **Never**: Put database queries in templates
10. **Never**: Hardcode sensitive data

---

**Happy Coding! 🚀**
