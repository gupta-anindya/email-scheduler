from celery import Celery
import time

# Celery setup
celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def send_email_later(email_data):
    time.sleep(5)  # Simulating delay
    return send_custom_email(email_data)

def schedule_email(email_data):
    # Call the Celery task for scheduling
    task = send_email_later.apply_async(args=[email_data], countdown=10)  # Email will be sent after 10 seconds
    return {"status": "Scheduled", "email": email_data['recipient'], "task_id": task.id}
