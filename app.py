import os
import logging
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
babel = Babel()
bcrypt = Bcrypt()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")  # Default for development
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # Needed for url_for to generate with https

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///sales_reports.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure uploads
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload
app.config["ALLOWED_EXTENSIONS"] = {"csv", "xlsx", "xls", "pdf"}

# Configure login manager
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

# Configure Babel localization settings
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ar']

# Function to get the user's locale
def get_locale():
    # Get locale from session or default to English
    return session.get('language', 'en')

# Configure Babel for localization
babel.init_app(app, locale_selector=get_locale)

# Initialize bcrypt for password hashing
bcrypt.init_app(app)

# Create upload folder if it doesn't exist
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# Import and register routes after app initialization to avoid circular imports
with app.app_context():
    # Import models to ensure tables are created
    from models import User, Report  # noqa: F401
    db.init_app(app)
    
    # Drop all tables and recreate them to apply model changes
    db.drop_all()
    db.create_all()
    
    # Import routes
    from routes import setup_routes
    setup_routes(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
