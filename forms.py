from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, DateField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from models import User
from app import app

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use another or login.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ReportUploadForm(FlaskForm):
    # Replaced title with employee_name
    employee_name = StringField('Employee Name', validators=[DataRequired(), Length(max=128)])
    # Removed description field and period fields
    product_model = StringField('Product Model', validators=[DataRequired(), Length(max=128)])
    sale_price = FloatField('Sale Price', validators=[DataRequired(), NumberRange(min=0)])
    units_sold = IntegerField('Units Sold', validators=[DataRequired(), NumberRange(min=0)])
    total_sales = FloatField('Total Sales', validators=[DataRequired(), NumberRange(min=0)])
    # File field is removed per request
    submit = SubmitField('Submit Report')
