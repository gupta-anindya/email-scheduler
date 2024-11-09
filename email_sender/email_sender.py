# email_sender.py
import smtplib
from email.mime.text import MIMEText
import pandas as pd
import json

def send_custom_email(email_data):
    try:
        msg = MIMEText(email_data['content'])
        msg['Subject'] = email_data['subject']
        msg['From'] = email_data['sender']
        msg['To'] = email_data['recipient']

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_data['sender'], email_data['password'])
            server.sendmail(email_data['sender'], email_data['recipient'], msg.as_string())

        return {"status": "Success", "message": "Email sent successfully"}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}

def load_data(file_path):
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    else:
        data = pd.read_excel(file_path)
    return data
