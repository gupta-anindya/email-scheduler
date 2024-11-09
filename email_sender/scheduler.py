# scheduler.py
from celery import Celery
from email_sender import send_custom_email
import json
import time

app = Celery('scheduler', broker='redis://localhost:6379/0')

@app.task(rate_limit='50/m')
def schedule_email_task(email_data):
    delay = email_data.get('delay', 0)
    time.sleep(delay)
    result = send_custom_email(email_data)
    return result
