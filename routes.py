import os
import uuid
from datetime import datetime
from urllib.parse import urlparse
from flask import render_template, redirect, url_for, flash, request, session, jsonify, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from models import User, Report
from forms import ReportUploadForm  # Remove auth forms since we use Replit Auth
from translations import get_translations
from replit_auth import make_replit_blueprint, require_login

def setup_routes(app):
    
    # Register Replit Auth blueprint
    app.register_blueprint(make_replit_blueprint(), url_prefix="/auth")
    
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
    
    # Redirect old register route to Replit Auth
    @app.route('/register')
    def register():
        return redirect(url_for('replit_auth.login'))
    
    # Redirect old login route to Replit Auth
    @app.route('/login')
    def login():
        return redirect(url_for('replit_auth.login'))
    
    # Redirect old logout route to Replit Auth
    @app.route('/logout')
    def logout():
        return redirect(url_for('replit_auth.logout'))
    
    # Route for user dashboard
    @app.route('/dashboard')
    @require_login
    def dashboard():
        translations = get_translations(session.get('language', 'en'))
        recent_reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).limit(5).all()
        return render_template('dashboard.html', reports=recent_reports, translations=translations, now=datetime.now())
    
    # Route for report upload
    @app.route('/upload', methods=['GET', 'POST'])
    @require_login
    def upload_report():
        translations = get_translations(session.get('language', 'en'))
        form = ReportUploadForm()
        
        # Pre-fill employee name with current user's display name
        if request.method == 'GET':
            form.employee_name.data = current_user.display_name
        
        if form.validate_on_submit():
            # Create report record with simplified fields
            report = Report()
            report.employee_name = form.employee_name.data
            report.product_model = form.product_model.data
            report.sale_price = form.sale_price.data
            report.units_sold = form.units_sold.data
            report.total_sales = form.total_sales.data
            report.user_id = current_user.id
            db.session.add(report)
            db.session.commit()
            
            flash(translations['report_uploaded'], 'success')
            return redirect(url_for('reports'))
                
        return render_template('upload_report.html', form=form, translations=translations, now=datetime.now())
    
    # Route for listing reports
    @app.route('/reports')
    @require_login
    def reports():
        translations = get_translations(session.get('language', 'en'))
        user_reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).all()
        return render_template('reports.html', reports=user_reports, translations=translations, now=datetime.now())
    
    # Route for report details
    @app.route('/reports/<int:report_id>')
    @require_login
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
    @require_login
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
        
        # Validate referrer URL to prevent open redirect attacks
        if request.referrer:
            parsed_referrer = urlparse(request.referrer)
            # Only redirect if it's a relative URL or same domain
            if not parsed_referrer.netloc or parsed_referrer.netloc == request.host:
                return redirect(request.referrer)
        
        return redirect(url_for('index'))
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        translations = get_translations(session.get('language', 'en'))
        return render_template('error.html', error_code=404, error_message=translations['not_found'], now=datetime.now(), translations=translations), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        translations = get_translations(session.get('language', 'en'))
        return render_template('error.html', error_code=500, error_message=translations['server_error'], now=datetime.now(), translations=translations), 500
