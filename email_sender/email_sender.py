import smtplib
from email.mime.text import MIMEText
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

def send_custom_email(email_data):
    try:
        # Construct email message
        msg = MIMEText(email_data['content'])
        msg['Subject'] = email_data['subject']
        msg['From'] = email_data['sender']
        msg['To'] = email_data['recipient']

        # Using SMTP for email sending with OAuth2 or stored password
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            if email_data.get("oauth_token"):
                # Use OAuth2 token
                server.auth("XOAUTH2", lambda x: email_data['oauth_token'])
            else:
                # Use regular password authentication
                server.login(email_data['sender'], EMAIL_PASSWORD)
            server.sendmail(email_data['sender'], email_data['recipient'], msg.as_string())
        
        return {"status": "Success", "message": "Email sent successfully"}
    except smtplib.SMTPAuthenticationError:
        return {"status": "Failed", "error": "Authentication error. Check email credentials or OAuth2 setup."}
    except smtplib.SMTPRecipientsRefused:
        return {"status": "Failed", "error": "Recipient address was refused by the server."}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}

def load_data(file_path):
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    else:
        data = pd.read_excel(file_path)
    return data

def connect_google_sheet(sheet_id, range_name="Sheet1"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/service_account.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).worksheet(range_name)
    data = sheet.get_all_records()
    return data

def dynamic_email_content(prompt_template, row_data):
    """ Customize email content by replacing placeholders with data from each row. """
    return prompt_template.format(**row_data)

def generate_email_content(prompt_template, row_data):
    """ Integrate with the Groq API to generate customized email content. """
    prompt = prompt_template.format(**row_data)
    
    response = requests.post(
        "https://api.groq.com/v1/generate",
        json={"prompt": prompt},
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"}
    )
    
    if response.status_code == 200:
        return response.json().get("generated_text")
    else:
        return f"Error generating content: {response.status_code}"

def get_oauth2_token(client_secrets_file, token_file, scopes):
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return creds.token
