from flask import Flask, request, render_template, jsonify
from email_sender import (
    send_custom_email,
    load_data,
    connect_google_sheet,
    dynamic_email_content,
    generate_email_content,
    get_oauth2_token
)
from scheduler import schedule_email_task
import os
import json
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    email_data = request.json
    result = send_custom_email(email_data)
    return jsonify(result)

@app.route('/generate_content', methods=['POST'])
def generate_content():
    data = request.json
    template = data.get('template')
    row_data = data.get('row_data')
    # Generate AI-based email content
    content = generate_email_content(template, row_data)
    return jsonify({"content": content})

@app.route('/get_oauth_token', methods=['GET'])
def oauth_token():
    # Example OAuth2 setup with Gmail
    token = get_oauth2_token('path/to/client_secrets.json', 'token.json', ["https://mail.google.com/"])
    return jsonify({"token": token})

@app.route('/schedule_email', methods=['POST'])
def schedule_email():
    schedule_data = request.json
    result = schedule_email_task.apply_async((schedule_data,))
    return jsonify({"status": "Scheduled", "task_id": result.id})

if __name__ == "__main__":
    app.run(debug=True)
