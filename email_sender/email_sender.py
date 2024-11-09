import smtplib
from email.mime.text import MIMEText
import os

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
        
        return {"status": "Success", "message": "Email sent successfully", "email": email_data['recipient']}
    except smtplib.SMTPAuthenticationError:
        return {"status": "Failed", "error": "Authentication error. Check email credentials or OAuth2 setup.", "email": email_data['recipient']}
    except smtplib.SMTPRecipientsRefused:
        return {"status": "Failed", "error": "Recipient address was refused by the server.", "email": email_data['recipient']}
    except Exception as e:
        return {"status": "Failed", "error": str(e), "email": email_data['recipient']}
