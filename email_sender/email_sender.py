import smtplib
from email.mime.text import MIMEText
import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
import requests

def connect_google_sheet(sheet_url):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_creds.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url)
    return sheet.get_all_records()

def read_csv(file_path):
    return pd.read_csv(file_path).to_dict(orient='records')

def generate_email_content(prompt, row_data):
    prompt_filled = prompt.format(**row_data)
    response = requests.post(
        "https://api.groq.com/v1/generate",
        json={"prompt": prompt_filled},
        headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"}
    )
    return response.json().get('generated_text')

def send_email(email_data):
    msg = MIMEText(email_data['content'])
    msg['Subject'] = email_data['subject']
    msg['From'] = email_data['sender']
    msg['To'] = email_data['recipient']
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_data['sender'], os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)

def send_emails(data_source, prompt_template):
    data = connect_google_sheet(data_source) if data_source.endswith('google.com') else read_csv(data_source)
    for row in data:
        email_content = generate_email_content(prompt_template, row)
        send_email({
            'content': email_content,
            'subject': 'Your Custom Email',
            'sender': 'your-email@gmail.com',
            'recipient': row['Email']
        })
