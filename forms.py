from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, URL, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    price = FloatField('Price', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Price must be greater than 0')
    ])
    category = StringField('Category', validators=[
        DataRequired()
    ])
    description = TextAreaField('Description', validators=[
        DataRequired()
    ])
    image_url = StringField('Image URL', validators=[
        DataRequired(),
        URL(message='Must be a valid URL')
    ])
    stock = IntegerField('Stock', validators=[
        DataRequired(),
        NumberRange(min=0, message='Stock cannot be negative')
    ])
    submit = SubmitField('Save Product')
