"""authentication related urls
"""
from .models import User, db
from  flask import Flask,redirect, current_app, url_for, render_template, request, Blueprint, current_app, session, flash, make_response
from flask_login import login_required, login_user, current_user, logout_user
from . import cache
from flask_babel import _
from flask_babel import gettext
import uuid
import bcrypt
from . import redis_client
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from . import mail
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/',methods=['GET','POST'])
def home():
    """home page
    """
    return render_template('index.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """provides the registration functionality for new user
    """
    if request.method == 'POST':
        username = request.form['username']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Password does not much', 'error')
        
        user = User.query.filter_by(email=email, phone_number=phone_number).first()
        if user:
            flash('User already registered')
        else:
           salt = bcrypt.gensalt()
           hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
           
           user = User(username=username, email=email, middle_name=middle_name, phone_number=phone_number, last_name=last_name, password_hash=hashed_password)
           db.session.add(user)
           db.session.commit()
           flash("User registered successfully!")
           return redirect(url_for('auth.login'))

    return render_template('register.html')

def send_password_reset_email(email):
    """Sends password reset email
    """
    serializer = URLSafeTimedSerializer(current_app.config[ 'SECRET_KEY' ])
    token = serializer.dumps(email, salt=current_app.config[ 'SECURITY_PASSWORD_SALT' ])
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    msg = Message('Password Reset Request', sender='yakobbonke@gmail.com', recipients=[email])
    msg.body = f"Please click the following link to reset your password: {reset_url}"
    mail.send(msg)

@auth_bp.route('/reset-password_request', methods=['GET', 'POST'])
def reset_password_request():
    """queries email from database and calls the function sending reset link
    """
    if request.method == 'POST':
        email = request.form.get('email')

        user = User.query.filter_by(email=email).first()
        if user:
            send_password_reset_email(email)
            flash('Password reset instructions have been sent to your email.')
            return redirect('/login')  
        else:
            flash('No user with that email address exists.')
            return redirect('/reset-password')  
    return render_template('reset_password_request.html')


class ResetPasswordForm(FlaskForm):
    """password reseting
    """
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')

@auth_bp.route('/reset_password/', defaults={'token': None}, methods=['GET', 'POST'])
@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """resets password
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=3600)
    except SignatureExpired:
        flash('The password reset link has expired.')
        return redirect(url_for('auth.login'))
    except:
        flash('Invalid password reset link.')
        return redirect(url_for('auth.login'))

    form = ResetPasswordForm()  

    if form.validate_on_submit():
        if form.new_password.data != form.confirm_password.data:
            flash('Passwords do not match.')
            return redirect(url_for('auth.reset_password', token=token))

        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been reset successfully.')
            return redirect(url_for('auth.login'))

    return render_template('reset_password.html', form=form, token=token)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """login view
    """
    if request.method == 'POST':
        email = request.form['email_or_phone']
        password = request.form['password']
        remember = False
        
        if 'remember_password' in request.form and request.form['remember_password'] == 'true':
            remember = True
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            login_user(user, remember=remember)
             
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            flash('Logged in successfully', category='success')
            return redirect(url_for('auth.portal'))
        else:
            flash('Incorrect username or password. Please try again.', category='error')
    
    return render_template('login.html')
@auth_bp.route('/portal')
def portal():
    
    if current_user.is_authenticated:
        return render_template('portal.html')
    else:
        flash('You must log in to access the portal.', 'warning')
        return redirect('login')
    
@auth_bp.route('/logout')
@login_required
def logout():
    session.pop('session_id', None) 
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))
@auth_bp.route('/profile', methods=['GET','POST'])
def profile():
    
    user = User.query.all()
    return render_template('profile.html', user=user) 