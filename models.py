from datetime import datetime
from app import db
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy import UniqueConstraint


# (IMPORTANT) This table is mandatory for Replit Auth, don't drop it.
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    profile_image_url = db.Column(db.String, nullable=True)
    
    # Keep existing fields for backward compatibility
    username = db.Column(db.String(64), unique=True, nullable=True)  # Made nullable for Replit Auth users
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    reports = db.relationship('Report', backref='user', lazy='dynamic')

    # Keep user roles and approval for existing functionality
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_approved = db.Column(db.Boolean, default=True, nullable=False)  # Auto-approve Replit Auth users
    approval_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.username or self.email}>'

    def is_administrator(self):
        """Check if the user has admin privileges"""
        return self.is_admin

    def is_account_approved(self):
        """Check if the user account has been approved by an admin"""
        return self.is_approved

    @property
    def display_name(self):
        """Get display name for the user"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.username:
            return self.username
        else:
            return self.email or "Unknown User"


# (IMPORTANT) This table is mandatory for Replit Auth, don't drop it.
class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.String, db.ForeignKey(User.id))
    browser_session_key = db.Column(db.String, nullable=False)
    user = db.relationship(User)

    __table_args__ = (UniqueConstraint(
        'user_id',
        'browser_session_key',
        'provider',
        name='uq_user_browser_session_key_provider',
    ),)


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
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    # Link to user who created the report
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Report {self.employee_name} - {self.product_model}>'