"""all flask-extensions initialized
"""
import os
from urllib.parse import quote
from flask import Flask, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_babel import _, Babel
from flask_caching import Cache
from flask_migrate import Migrate
from datetime import timedelta
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import redis


db = SQLAlchemy()
cache = Cache()
login_manager = LoginManager()
migrate = Migrate()
babel = Babel()
mail = Mail()

redis_client = redis.Redis(host='localhost', port=6379)

def register_extensions(app, cache):
    # cache.init_app(app)
    app.cache = cache


def create_app():
    """creates app and initializes extensions within the app context
    """
    app = Flask(__name__)

    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['REDIS_CLIENT'] = redis_client
    
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)
    
    
    db_password = os.environ.get('DB_PASSWORD')
    if not db_password:
        raise ValueError("DB_PASSWORD environment variable is not set or is empty.")

    encoded_password = quote(db_password.encode('utf-8'))
    db_url = f"mysql+mysqldb://James:{encoded_password}@localhost/website"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
    babel.init_app(app)

    app.config['LANGUAGES'] = {
        'en': 'English',
        'am': 'Amharic'
    }
    app.config['BABEL_DOMAIN'] = 'message'
    app.config['BABEL_DATE_FORMATS'] = {
        'en': 'MM/dd/yyyy',
        'am': 'dd/MM/yyyy'
    }

    app.config['BABEL_TIME_FORMATS'] = {
        'en': 'h:mm a',
        'am': 'HH:mm'
    }

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(
            app.config['LANGUAGES'].keys())
    babel.locale_selector_func = get_locale

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        """Retrieve the user object based on the user_id"""
        return User.query.get(user_id)
    
    from .library import library_bp
    from .main import main_bp
    from .auth import auth_bp
    from .cart import course_bp
    from .add_to_db import add_to_db_bp
    from .departments import department_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(library_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(add_to_db_bp)
    app.register_blueprint(department_bp)

    register_extensions(app, cache)

    db.init_app(app)
    cache.init_app(app)
    login_manager.init_app(app)
    
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'jackmanbonke@gmail.com'
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')
    mail = Mail(app)
    
    return app