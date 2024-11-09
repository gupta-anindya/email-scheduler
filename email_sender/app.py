from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from email_sender import send_custom_email
from scheduler import schedule_email
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Route to the dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Trigger email send via WebSocket
@socketio.on('send_email')
def handle_send_email(data):
    """
    Handle the email sending request, then emit a status back to the client.
    """
    result = send_custom_email(data)
    emit('email_status', result)  # Emit status to frontend in real-time

# Trigger email scheduling via WebSocket
@socketio.on('schedule_email')
def handle_schedule_email(data):
    """
    Handle the email scheduling request, then emit a status back to the client.
    """
    result = schedule_email(data)  # Call Celery task
    emit('email_status', result)  # Emit status to frontend in real-time

if __name__ == '__main__':
    socketio.run(app, debug=True)
