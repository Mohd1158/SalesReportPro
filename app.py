import os
import logging
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')

# إعدادات اللوجينق
logging.basicConfig(level=logging.DEBUG)

# تعريف Base class للـ SQLAlchemy
class Base(DeclarativeBase):
    pass

# تهيئة الإضافات
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
babel = Babel()
bcrypt = Bcrypt()

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# إعدادات قاعدة البيانات
database_url = os.environ.get("DATABASE_URL", "sqlite:///sales_reports.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# إعدادات رفع الملفات
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB
app.config["ALLOWED_EXTENSIONS"] = {"csv", "xlsx", "xls", "pdf"}

# إعداد login manager
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

# إعداد التعدد اللغوي
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ar']

def get_locale():
    return session.get('language', 'en')

babel.init_app(app, locale_selector=get_locale)
bcrypt.init_app(app)

# إنشاء مجلد الرفع إذا لم يكن موجود
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# تهيئة قاعدة البيانات (مرة واحدة فقط)
with app.app_context():
    from models import User, Report  # noqa: F401
    db.init_app(app)
    db.create_all()  # لا تستخدم db.drop_all() أبداً هنا

# استيراد وتسجيل المسارات
from routes import setup_routes
setup_routes(app)

# تحميل المستخدمين للدخول
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
