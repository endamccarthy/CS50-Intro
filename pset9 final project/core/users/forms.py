import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from core.models import User
from core import bcrypt


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_password(self, password):
        while True:
            if len(password.data) < 8:
                raise ValidationError("Make sure your password is at least 8 letters.")
            elif re.search('[0-9]',password.data) is None:
                raise ValidationError("Make sure your password has a number in it.")
            elif re.search('[A-Z]',password.data) is None: 
                raise ValidationError("Make sure your password has a capital letter in it.")
            else:
                break


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Current Password')
    new_password = PasswordField('New Password')
    confirm_new_password = PasswordField('Confirm New Password', validators=[EqualTo('new_password', message='Passwords must match.')])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

    def validate_password(self, password):
        if password.data:
            if not bcrypt.check_password_hash(current_user.password, password.data):
                raise ValidationError('That password is incorrect. Please try again.')

    def validate_new_password(self, new_password):
        if new_password.data:
            while True:
                if len(new_password.data) < 8:
                    raise ValidationError("Make sure your password is at least 8 letters.")
                elif re.search('[0-9]',new_password.data) is None:
                    raise ValidationError("Make sure your password has a number in it.")
                elif re.search('[A-Z]',new_password.data) is None: 
                    raise ValidationError("Make sure your password has a capital letter in it.")
                else:
                    break


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

    def validate_password(self, password):
        while True:
            if len(password.data) < 8:
                raise ValidationError("Make sure your password is at least 8 letters")
            elif re.search('[0-9]',password.data) is None:
                raise ValidationError("Make sure your password has a number in it")
            elif re.search('[A-Z]',password.data) is None: 
                raise ValidationError("Make sure your password has a capital letter in it")
            else:
                break