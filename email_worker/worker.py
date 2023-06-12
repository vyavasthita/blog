import os
from celery import Celery
from email_worker.config import config_by_name


environment = os.getenv('FLASK_ENV') or 'development'
config = config_by_name[environment]


app = Celery('email', broker=config['CELERY_BROKER_URL'], backend=config['CELERY_RESULT_BACKEND'])


@app.task(name='email.send')
def send_email(sender: str, to: str, subject: str, template: str) -> tuple:
    print(f"Sender {sender}, Receiver {to}, Subject {subject}")

    # Success/failure, Message, Result
    return True, None, None