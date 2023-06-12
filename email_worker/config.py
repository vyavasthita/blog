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


devlopment_config = dict(
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL_DEV'),
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND_DEV'),
    MAIL_SERVER = os.getenv('MAIL_SERVER_DEV'),
    MAIL_PORT = ast.literal_eval(os.getenv('MAIL_PORT_DEV')),
    MAIL_USE_TLS = ast.literal_eval(os.getenv('MAIL_USE_TLS_DEV')),
    MAIL_USE_SSL = ast.literal_eval(os.getenv('MAIL_USE_SSL_DEV')),
    MAIL_USERNAME = os.getenv('MAIL_USERNAME_DEV'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD_DEV')
)
    
aut_testing_config = dict(
    MAIL_USERNAME = os.getenv('MAIL_USERNAME_AUT_TESTING'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD_AUT_TESTING'),
    MAIL_SERVER = os.getenv('MAIL_SERVER_AUT_TESTING'),
    MAIL_PORT = ast.literal_eval(os.getenv('MAIL_PORT_AUT_TESTING')),
    MAIL_USE_TLS = ast.literal_eval(os.getenv('MAIL_USE_TLS_AUT_TESTING')),
    MAIL_USE_SSL = ast.literal_eval(os.getenv('MAIL_USE_SSL_AUT_TESTING')),
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL_AUT_TESTING'),
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND_AUT_TESTING')
)

config_by_name = dict(
    development=devlopment_config,
    automated_testing=aut_testing_config
)
