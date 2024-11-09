from celery import Celery
from email_sender import send_emails
import datetime

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def schedule_emails(data_source, prompt_template, schedule_time):
    delay = (datetime.datetime.strptime(schedule_time, '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()).total_seconds()
    app.send_task('tasks.send_emails', args=[data_source, prompt_template], countdown=delay)
