# Sales Reports Manager

## Overview

The Sales Reports Manager is a Flask-based web application designed to streamline the sales reporting process for businesses. The application allows users to create, manage, and organize sales reports with detailed product and sales information. It features a modern, responsive interface with multi-language support (English and Arabic) and integrates with Replit's authentication system for secure user management.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive UI
- **Theme**: Replit's dark theme with custom CSS styling
- **Multi-language Support**: Built-in internationalization with English and Arabic translations
- **Client-side Interactivity**: Vanilla JavaScript for form handling, tooltips, and dynamic interactions
- **Responsive Design**: Mobile-first approach using Bootstrap's grid system

### Backend Architecture
- **Framework**: Flask with modular design using blueprints
- **Database ORM**: SQLAlchemy with declarative base for model definitions
- **Form Handling**: WTForms with Flask-WTF for form validation and CSRF protection
- **Authentication**: Replit Auth OAuth2 integration with fallback user management
- **Session Management**: Flask sessions with secure secret key configuration
- **File Upload**: Werkzeug secure filename handling with configurable upload limits

### Data Models
- **User Model**: Supports both Replit Auth users and legacy username-based accounts with admin roles and approval system
- **Report Model**: Stores sales data including employee information, product details, pricing, and sales metrics
- **OAuth Model**: Manages OAuth tokens for Replit authentication

### Security Features
- **CSRF Protection**: Flask-WTF CSRF tokens on all forms
- **Secure File Uploads**: File type validation and secure filename handling
- **Session Security**: Configurable session secret key
- **User Authorization**: Role-based access control with admin privileges
- **Proxy Fix**: Werkzeug proxy fix for proper HTTPS URL generation

### Application Structure
- **Modular Design**: Separate files for models, forms, routes, and authentication
- **Configuration Management**: Environment-based configuration for database URLs and secrets
- **Error Handling**: Custom error pages with user-friendly messages
- **Logging**: Configurable logging system for debugging and monitoring

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework with SQLAlchemy extension
- **Flask-Login**: User session management
- **Flask-Babel**: Internationalization support
- **Flask-WTF**: Form handling and validation
- **WTForms**: Form field validation and rendering

### Database
- **SQLAlchemy**: ORM for database operations
- **Database Support**: Configurable database URL with PostgreSQL and SQLite support
- **Connection Pooling**: Configured with pool recycling and pre-ping for reliability

### Authentication System
- **Replit Auth**: OAuth2 integration using Flask-Dance
- **JWT**: Token handling for OAuth authentication
- **Flask-Dance**: OAuth consumer blueprint for Replit integration

### Frontend Libraries
- **Bootstrap 5**: UI framework with Replit's dark theme
- **Font Awesome**: Icon library for UI elements
- **Bootstrap JavaScript**: Interactive components (tooltips, modals, dropdowns)

### File Processing
- **Werkzeug**: Secure file upload handling
- **File Type Support**: CSV, Excel (xlsx, xls), and PDF file validation
- **Upload Limits**: 16MB maximum file size with configurable extensions

### Development and Deployment
- **Environment Configuration**: Support for DATABASE_URL and SESSION_SECRET environment variables
- **Proxy Compatibility**: Configured for deployment behind reverse proxies
- **Static File Serving**: Flask static file handling for CSS, JavaScript, and assets