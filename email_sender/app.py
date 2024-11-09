# app.py
from flask import Flask, request, render_template, jsonify
from email_sender import send_custom_email
from scheduler import schedule_email
import json
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
def schedule():
    schedule_data = request.json
    result = schedule_email(schedule_data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
