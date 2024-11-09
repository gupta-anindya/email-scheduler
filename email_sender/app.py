from flask import Flask, request, render_template, jsonify
from email_sender import send_custom_email, load_data, connect_google_sheet, dynamic_email_content
from scheduler import schedule_email_task
import json
import sqlite3
import pandas as pd

app = Flask(__name__)

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    email_data = request.json
    result = send_custom_email(email_data)
    return jsonify(result)

@app.route('/schedule_email', methods=['POST'])
def schedule_email():
    schedule_data = request.json
    result = schedule_email_task.apply_async((schedule_data,))
    return jsonify({"status": "Scheduled", "task_id": result.id})

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files['file']
    data = pd.read_csv(file)
    return jsonify({"status": "success", "data": data.to_dict()})

@app.route('/webhook', methods=['POST'])
def webhook():
    event_data = request.json
    # Process delivery statuses
    # Update statuses in the database if needed
    return jsonify({"status": "received"})

if __name__ == "__main__":
    app.run(debug=True)
