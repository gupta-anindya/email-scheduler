# scheduler.py
from celery import Celery
from email_sender import send_custom_email
import time
import json

app = Celery('scheduler', broker='redis://localhost:6379/0')

@app.task
def schedule_email(email_data):
    delay = email_data.get('delay', 0)
    time.sleep(delay)
    result = send_custom_email(email_data)
    return result
