from datetime import datetime
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reports = db.relationship('Report', backref='user', lazy='dynamic')
    
    # New fields for user roles and approval
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    approval_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'
        
    def is_administrator(self):
        """Check if the user has admin privileges"""
        return self.is_admin
        
    def is_account_approved(self):
        """Check if the user account has been approved by an admin"""
        return self.is_approved

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Changed title to employee_name
    employee_name = db.Column(db.String(128), nullable=False)
    # Removed description, file fields, and period fields
    
    # Sales data fields (now required)
    product_model = db.Column(db.String(128), nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    units_sold = db.Column(db.Integer, nullable=False)
    total_sales = db.Column(db.Float, nullable=False)
    
    # Automatically set dates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Link to user who created the report
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Report {self.employee_name} - {self.product_model}>'
