from flask import Flask, render_template, request, redirect, url_for, flash
from email_sender import send_emails
from scheduler import schedule_emails
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'my_secret_key')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('dashboard'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('dashboard'))
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        flash('File uploaded successfully')
        return redirect(url_for('dashboard'))

@app.route('/send_emails', methods=['POST'])
def send_email_route():
    data_source = request.form['data_source']
    prompt_template = request.form['prompt']
    send_emails(data_source, prompt_template)
    flash('Emails sent successfully')
    return redirect(url_for('dashboard'))

@app.route('/schedule_emails', methods=['POST'])
def schedule_email_route():
    schedule_time = request.form['schedule_time']
    data_source = request.form['data_source']
    prompt_template = request.form['prompt']
    schedule_emails(data_source, prompt_template, schedule_time)
    flash('Emails scheduled successfully')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
