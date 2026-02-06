"""
Banner Model
"""
from app import db
from sqlalchemy.sql import func

class Banner(db.Model):
    """Banner generation history model"""
    __tablename__ = 'banner'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Banner specifications
    size = db.Column(db.String(50), nullable=False)
    
    # Text content
    company_name = db.Column(db.String(200))
    product_name = db.Column(db.String(200))
    subtext = db.Column(db.Text)
    website = db.Column(db.String(200))
    call_to_action = db.Column(db.String(100))
    discount = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    
    # Image data stored as BLOB
    banner_image = db.Column(db.LargeBinary, nullable=False)
    background_image = db.Column(db.LargeBinary)
    logo_image = db.Column(db.LargeBinary)
    product_image = db.Column(db.LargeBinary)
    
    # Image paths (backup reference)
    background_path = db.Column(db.String(500))
    logo_path = db.Column(db.String(500))
    product_path = db.Column(db.String(500))
    generated_banner_path = db.Column(db.String(500))
    
    # Metadata
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    
    def __repr__(self):
        return f'<Banner {self.id} - {self.size} - User {self.user_id}>'
