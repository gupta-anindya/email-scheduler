import os
import smtplib
import sqlite3
import requests
import pandas as pd
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the database
def initialize_db():
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS emails (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        recipient TEXT,
                        subject TEXT,
                        content TEXT,
                        status TEXT,
                        scheduled_time DATETIME)''')
    conn.commit()
    conn.close()

# Function to generate email content using Groq API
def generate_email_content(prompt_template, row_data):
    prompt = prompt_template.format(**row_data)
    response = requests.post(
        "https://api.groq.com/v1/generate",
        json={"prompt": prompt},
        headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"}
    )
    if response.status_code == 200:
        return response.json().get("generated_text")
    else:
        return f"Error generating content: {response.status_code}"

# Function to get OAuth2 token (for secure email authentication)
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

# Function to send custom email with error handling
def send_custom_email(email_data):
    try:
        msg = MIMEText(email_data['content'])
        msg['Subject'] = email_data['subject']
        msg['From'] = email_data['sender']
        msg['To'] = email_data['recipient']

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            if email_data.get("oauth_token"):
                server.auth("XOAUTH2", lambda x: email_data['oauth_token'])
            else:
                server.login(email_data['sender'], os.getenv("EMAIL_PASSWORD"))
            server.sendmail(email_data['sender'], email_data['recipient'], msg.as_string())
        
        return {"status": "Success", "message": "Email sent successfully"}
    except smtplib.SMTPAuthenticationError:
        return {"status": "Failed", "error": "Authentication error. Check email credentials or OAuth2 setup."}
    except smtplib.SMTPRecipientsRefused:
        return {"status": "Failed", "error": "Recipient address was refused by the server."}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}

# Function to load data from CSV or Google Sheets
def load_data(file_path=None, sheet_id=None):
    if file_path:
        # Read data from a CSV file
        data = pd.read_csv(file_path)
    elif sheet_id:
        # Read data from Google Sheets
        import gspread
        gc = gspread.service_account(filename='path-to-your-service-account.json')
        worksheet = gc.open_by_key(sheet_id).sheet1
        data = pd.DataFrame(worksheet.get_all_records())
    else:
        return None
    
    return data

# Function to schedule email (with Celery and Redis)
from celery import Celery
app = Celery('email_sender', broker='redis://localhost:6379/0')

@app.task
def schedule_email(email_data):
    result = send_custom_email(email_data)
    # Store the email status in the database
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO emails (recipient, subject, content, status, scheduled_time) 
                      VALUES (?, ?, ?, ?, ?)''', 
                   (email_data['recipient'], email_data['subject'], email_data['content'], 
                    result['status'], email_data.get('scheduled_time')))
    conn.commit()
    conn.close()
    return result

# Function to send emails from the loaded data
def send_bulk_emails(file_path=None, sheet_id=None, prompt_template=None):
    data = load_data(file_path, sheet_id)
    if data is not None:
        for index, row in data.iterrows():
            email_content = generate_email_content(prompt_template, row)
            email_data = {
                'sender': os.getenv("SENDER_EMAIL"),
                'recipient': row['email'],  # Assuming 'email' is a column in your data
                'subject': 'Your Customized Email Subject',
                'content': email_content
            }
            schedule_email.apply_async((email_data,), countdown=5)  # Delay emails by 5 seconds for testing
        return {"status": "Success", "message": "Emails scheduled successfully"}
    else:
        return {"status": "Failed", "message": "No data found"}

# Initialize the database on script start
initialize_db()

if __name__ == '__main__':
    # Example usage
    prompt_template = "Dear {Company Name} team, we noticed that you have a strong presence in {Location}. Here's a proposal for collaboration."
    result = send_bulk_emails(file_path='contacts.csv', prompt_template=prompt_template)
    print(result)
