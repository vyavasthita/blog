"""Flask App Configuration.

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file config.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 3rd Jun 2023

About; -
--------
    It is responsible for setting all configurations required for flask app.

Working; -
----------
    This configuration class is initialized at the time of creating flask app.

Uses; -
-------
    All other python modules can use this class for accessing configurations.

Reference; -
------------
    TBD
"""
import os
import ast
from dotenv import load_dotenv


# The root directory
base_dir = os.path.abspath(os.path.dirname(__name__))

env_by_name = dict(
    development='.env.dev',
    automated_testing='.env.aut_test'
)

environment = os.getenv('FLASK_ENV')

if environment is None:
    print(f"'FLASK_ENV' environment variable is not set. Please set it among environments {env_by_name.keys()}")

if environment not in env_by_name.keys():
    print(f"Invalid {environment}. Available Environments {env_by_name.keys()}")

print("Using 'development' environment.")

environment = 'development'

for environment_file in env_by_name.values():
    load_dotenv(dotenv_path = os.path.join(base_dir, environment_file)) # to load .env file. .flaskenv file is automatically loaded without using load_dotenv()


class DevelopmentConfig:
    # Flaks CLI configurations
    FLASK_APP = os.getenv('FLASK_APP_DEV')
    FLASK_ENV = os.getenv('FLASK_ENV_DEV')
    DEBUG = ast.literal_eval(os.getenv('DEBUG_DEV'))
    TESTING = ast.literal_eval(os.getenv('TESTING_DEV'))
    FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST_DEV')
    FLASK_RUN_PORT = os.getenv('FLASK_RUN_PORT_DEV')

    # App Configurations
    DB_TYPE = os.getenv('DB_TYPE_DEV')

    SECRET_KEY = os.getenv('SECRET_KEY_DEV')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT_DEV')

    EMAIL_TOKEN_EXPIRATION = ast.literal_eval(os.getenv('EMAIL_TOKEN_EXPIRATION_DEV'))

    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER_DEV')
    
    MYSQL_USER = os.getenv('MYSQL_USER_DEV')
    MYSQL_HOST = os.getenv('MYSQL_HOST_DEV')
    MYSQL_DB = os.getenv('MYSQL_DB_DEV')
    MYSQL_PORT = os.getenv('MYSQL_PORT_DEV')

    if DB_TYPE == 'sqlite':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog_dev.db')
    else:
        # DATABASE url to be connected by the app
        SQLALCHEMY_DATABASE_URI = "mysql://" + MYSQL_USER + ":" + "@" + MYSQL_HOST + ":" + MYSQL_PORT + "/" + MYSQL_DB
        
    # We do not want to track the modifications done in the DB.
    SQLALCHEMY_TRACK_MODIFICATIONS = ast.literal_eval(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS_DEV', default = False))
    
    # The length of the randomely generated password
    PASSWORD_LENGTH = ast.literal_eval(os.getenv('PASSWORD_LENGTH_DEV'))

    # Configuration file for logging
    LOG_CONFIG_FILE = os.getenv('LOG_CONFIG_FILE_DEV') or './apps/config/logging.conf'

    # Directory where logs will be generated.
    LOGS_DIR = os.getenv('LOGS_DIR_DEV') or '/tmp/insurance_logs'

    # Log File name
    LOG_FILE_NAME = os.getenv('LOG_FILE_NAME_DEV') or 'insurance.log'

    # Celery Configuration
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL_DEV')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND_DEV')

    # mail settings
    MAIL_SERVER = os.getenv('MAIL_SERVER_DEV')
    MAIL_PORT = ast.literal_eval(os.getenv('MAIL_PORT_DEV'))
    MAIL_USE_TLS = ast.literal_eval(os.getenv('MAIL_USE_TLS_DEV'))
    MAIL_USE_SSL = ast.literal_eval(os.getenv('MAIL_USE_SSL_DEV'))

    # Email authentication
    MAIL_USERNAME = os.getenv('MAIL_USERNAME_DEV')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD_DEV')


class AutomatedTestingConfig:
    # Flaks CLI configurations
    FLASK_APP = os.getenv('FLASK_APP_AUT_TESTING')
    FLASK_ENV = os.getenv('FLASK_ENV_AUT_TESTING')
    DEBUG = ast.literal_eval(os.getenv('DEBUG_AUT_TESTING'))
    TESTING = ast.literal_eval(os.getenv('TESTING_AUT_TESTING'))
    FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST_AUT_TESTING')
    FLASK_RUN_PORT = os.getenv('FLASK_RUN_PORT_AUT_TESTING')

    # App Configurations
    DB_TYPE = os.getenv('DB_TYPE_AUT_TESTING')

    SECRET_KEY = os.getenv('SECRET_KEY_AUT_TESTING')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT_AUT_TESTING')

    EMAIL_TOKEN_EXPIRATION = ast.literal_eval(os.getenv('EMAIL_TOKEN_EXPIRATION_AUT_TESTING'))

    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER_AUT_TESTING')
    
    MYSQL_USER = os.getenv('MYSQL_USER_AUT_TESTING')
    MYSQL_HOST = os.getenv('MYSQL_HOST_AUT_TESTING')
    MYSQL_DB = os.getenv('MYSQL_DB_AUT_TESTING')
    MYSQL_PORT = os.getenv('MYSQL_PORT_AUT_TESTING')

    if DB_TYPE == 'sqlite':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog_aut_testing.db')
    else:
        # DATABASE url to be connected by the app
        SQLALCHEMY_DATABASE_URI = "mysql://" + MYSQL_USER + ":" + "@" + MYSQL_HOST + ":" + MYSQL_PORT + "/" + MYSQL_DB
        
    # We do not want to track the modifications done in the DB.
    SQLALCHEMY_TRACK_MODIFICATIONS = ast.literal_eval(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS_AUT_TESTING', default = False))
    
    # The length of the randomely generated password
    PASSWORD_LENGTH = ast.literal_eval(os.getenv('PASSWORD_LENGTH_AUT_TESTING'))

    # Configuration file for logging
    LOG_CONFIG_FILE = os.getenv('LOG_CONFIG_FILE_AUT_TESTING') or './apps/config/logging.conf'

    # Directory where logs will be generated.
    LOGS_DIR = os.getenv('LOGS_DIR_AUT_TESTING') or '/tmp/insurance_logs'

    # Log File name
    LOG_FILE_NAME = os.getenv('LOG_FILE_NAME_AUT_TESTING') or 'insurance.log'

    # Celery Configuration
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL_AUT_TESTING')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND_AUT_TESTING')

    # mail settings
    MAIL_SERVER = os.getenv('MAIL_SERVER_AUT_TESTING')
    MAIL_PORT = ast.literal_eval(os.getenv('MAIL_PORT_AUT_TESTING'))
    MAIL_USE_TLS = ast.literal_eval(os.getenv('MAIL_USE_TLS_AUT_TESTING'))
    MAIL_USE_SSL = ast.literal_eval(os.getenv('MAIL_USE_SSL_AUT_TESTING'))

    # Email authentication
    MAIL_USERNAME = os.getenv('MAIL_USERNAME_AUT_TESTING')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD_AUT_TESTING')


config_by_name = dict(
    development=DevelopmentConfig(),
    automated_testing=AutomatedTestingConfig()
)
