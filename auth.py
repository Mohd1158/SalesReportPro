from functools import wraps
from flask import redirect, url_for, session, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from models import User
from translations import get_translations

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login first.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login first.', 'warning')
            return redirect(url_for('login', next=request.url))
        if not current_user.is_admin:
            translations = get_translations(session.get('language', 'en'))
            flash(translations.get('access_denied', 'Access denied. Admin privileges required.'), 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def authenticate_user(email, password):
    """Authenticate user with email and password"""
    user = User.query.filter_by(email=email).first()
    if user and user.password_hash and check_password_hash(user.password_hash, password):
        return user
    return None

def register_user(username, email, password):
    """Register a new user"""
    # Check if user already exists
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        return None, "User already exists with this email or username"
    
    # Create new user
    user = User()
    user.id = f"user_{username}_{str(abs(hash(email)))[:8]}"
    user.username = username
    user.email = email
    user.password_hash = generate_password_hash(password)
    user.is_approved = True  # Auto-approve new users
    user.is_admin = False  # Default to non-admin
    
    # Make first user admin if no admin exists
    admin_count = User.query.filter_by(is_admin=True).count()
    if admin_count == 0:
        user.is_admin = True
    
    try:
        db.session.add(user)
        db.session.commit()
        return user, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)