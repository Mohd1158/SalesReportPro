import os
import uuid
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, session, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db, bcrypt
from models import User, Report
from forms import RegistrationForm, LoginForm, ReportUploadForm
from translations import get_translations

def setup_routes(app):
    
    # Helper function to check allowed file extensions
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
    # Context processor to add variables to all templates
    @app.context_processor
    def inject_template_vars():
        translations = get_translations(session.get('language', 'en'))
        return {
            'now': datetime.now(),
            'translations': translations
        }
               
    # Route for the home page
    @app.route('/')
    def index():
        translations = get_translations(session.get('language', 'en'))
        return render_template('index.html', translations=translations, now=datetime.now())
    
    # Route for user registration
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
            
        translations = get_translations(session.get('language', 'en'))
        form = RegistrationForm()
        
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=hashed_password
            )
            db.session.add(user)
            db.session.commit()
            flash(translations['account_created'], 'success')
            return redirect(url_for('login'))
            
        return render_template('register.html', form=form, translations=translations, now=datetime.now())
    
    # Route for user login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
            
        translations = get_translations(session.get('language', 'en'))
        form = LoginForm()
        
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                flash(translations['login_success'], 'success')
                return redirect(next_page if next_page else url_for('dashboard'))
            else:
                flash(translations['login_failed'], 'danger')
                
        return render_template('login.html', form=form, translations=translations, now=datetime.now())
    
    # Route for user logout
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        translations = get_translations(session.get('language', 'en'))
        flash(translations['logout_success'], 'success')
        return redirect(url_for('index'))
    
    # Route for user dashboard
    @app.route('/dashboard')
    @login_required
    def dashboard():
        translations = get_translations(session.get('language', 'en'))
        recent_reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).limit(5).all()
        return render_template('dashboard.html', reports=recent_reports, translations=translations, now=datetime.now())
    
    # Route for report upload
    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def upload_report():
        translations = get_translations(session.get('language', 'en'))
        form = ReportUploadForm()
        
        if form.validate_on_submit():
            # Create report record with simplified fields
            report = Report(
                employee_name=form.employee_name.data,
                product_model=form.product_model.data,
                sale_price=form.sale_price.data,
                units_sold=form.units_sold.data,
                total_sales=form.total_sales.data,
                user_id=current_user.id
            )
            db.session.add(report)
            db.session.commit()
            
            flash(translations['report_uploaded'], 'success')
            return redirect(url_for('reports'))
                
        return render_template('upload_report.html', form=form, translations=translations, now=datetime.now())
    
    # Route for listing reports
    @app.route('/reports')
    @login_required
    def reports():
        translations = get_translations(session.get('language', 'en'))
        user_reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).all()
        return render_template('reports.html', reports=user_reports, translations=translations, now=datetime.now())
    
    # Route for report details
    @app.route('/reports/<int:report_id>')
    @login_required
    def report_detail(report_id):
        translations = get_translations(session.get('language', 'en'))
        report = Report.query.get_or_404(report_id)
        
        # Check if report belongs to the current user
        if report.user_id != current_user.id:
            flash(translations['not_authorized'], 'danger')
            return redirect(url_for('reports'))
            
        return render_template('report_detail.html', report=report, translations=translations, now=datetime.now())
    
    # Export report functionality will be implemented later
    # Previously had download_report here
    
    # Route for deleting a report
    @app.route('/reports/<int:report_id>/delete', methods=['POST'])
    @login_required
    def delete_report(report_id):
        report = Report.query.get_or_404(report_id)
        translations = get_translations(session.get('language', 'en'))
        
        # Check if report belongs to the current user
        if report.user_id != current_user.id:
            flash(translations['not_authorized'], 'danger')
            return redirect(url_for('reports'))
            
        # Delete the record
        db.session.delete(report)
        db.session.commit()
        
        flash(translations['report_deleted'], 'success')
        return redirect(url_for('reports'))
    
    # Route for setting language
    @app.route('/set-language/<lang>')
    def set_language(lang):
        if lang in ['en', 'ar']:
            session['language'] = lang
        return redirect(request.referrer or url_for('index'))
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        translations = get_translations(session.get('language', 'en'))
        return render_template('error.html', error_code=404, error_message=translations['not_found'], now=datetime.now(), translations=translations), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        translations = get_translations(session.get('language', 'en'))
        return render_template('error.html', error_code=500, error_message=translations['server_error'], now=datetime.now(), translations=translations), 500
