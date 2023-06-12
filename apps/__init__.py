import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from celery import Celery
from config.config import config_by_name

environment = os.getenv('FLASK_ENV') or 'development'


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_log_directory():
    base_dir = os.path.abspath(os.path.dirname(__name__))

    if not os.path.exists(os.path.join(base_dir, configuration.LOGS_DIR)):
        print("Creating log directory.")
        os.mkdir(os.path.join(base_dir, configuration.LOGS_DIR))

def register_blueprint(app):
    from apps.user.views import user_blueprint
    app.register_blueprint(user_blueprint)

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[environment])

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    create_log_directory()
    
    print("Enabling CORS.")
    CORS(app)

    login_manager.init_app(app=app)
    login_manager.login_view = 'api.user_login'

    register_blueprint(app=app)
    
    return app

configuration = config_by_name[environment]

celery = Celery(__name__, broker=configuration.CELERY_BROKER_URL, 
                result_backend=configuration.CELERY_RESULT_BACKEND)