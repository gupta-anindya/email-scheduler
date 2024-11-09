---

# Custom Email Sender for BreakoutAI

This project is a custom email-sending application with scheduling, throttling, real-time tracking, and LLM-based content generation. It reads data from Google Sheets or CSV files, allows email account connections, customizes and sends AI-generated emails with dynamic fields, and tracks delivery statuses on a dashboard. The application includes secure credential management, OAuth2 support for secure email authentication, and enhanced error handling.

---

## Project Structure

```
email_sender/
├── app.py              # Main Flask app
├── email_sender.py     # Email sending functions, including Google Sheets and Groq API integration
├── scheduler.py        # Scheduling and throttling with Celery
├── config.json         # Configuration for ESP settings and API keys
├── templates/
│   └── dashboard.html  # Dashboard for real-time tracking
├── emails.db           # SQLite database for storing scheduled emails
└── README.md           # Project documentation
```

---

## Requirements

- Python 3.x
- [Flask](https://flask.palletsprojects.com/en/2.1.x/): `pip install Flask`
- [Celery](https://docs.celeryproject.org/en/stable/): `pip install celery`
- [Redis](https://redis.io/): for scheduling and throttling. Install via `redis-server`.
- [Pandas](https://pandas.pydata.org/): `pip install pandas`
- [gspread](https://gspread.readthedocs.io/en/latest/) and [oauth2client](https://pypi.org/project/oauth2client/): for Google Sheets integration, install via `pip install gspread oauth2client`
- [SendGrid](https://sendgrid.com/) or another ESP library if using SendGrid API.
- [Groq API](https://groq.com/) library for LLM integration.
- [google-auth](https://google-auth.readthedocs.io/) for OAuth2: `pip install google-auth google-auth-oauthlib google-auth-httplib2`
- [smtplib](https://docs.python.org/3/library/smtplib.html): included in Python standard library.

---

## Setup and Configuration

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd email_sender
```

### Step 2: Create a Virtual Environment and Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

For secure credential storage, configure environment variables for sensitive data like passwords and API keys.

Example:
```bash
export EMAIL_PASSWORD="your-email-password"
export GROQ_API_KEY="your-groq-api-key"
export SENDGRID_API_KEY="your-sendgrid-api-key"
```

### Step 4: Configure `config.json`

In the `config.json` file, specify the ESP (e.g., SendGrid) API key.

Example configuration for Gmail:
```json
{
  "email_sender": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 465,
    "email": "your-email@gmail.com",
    "password": "your-email-password"
  },
  "esp": {
    "sendgrid_api_key": "YOUR_SENDGRID_API_KEY"
  }
}
```

### Step 5: Google Sheets API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Sheets API** and **Google Drive API**.
3. Create a **Service Account** and download the JSON key file.
4. Place this JSON file in your project and update the path in `email_sender.py`.

### Step 6: Start Redis Server

Ensure Redis is running. Start Redis in a new terminal window:

```bash
redis-server
```

### Step 7: Start Celery Worker

Open another terminal and navigate to the project directory, then run:

```bash
celery -A scheduler worker --loglevel=info
```

### Step 8: Run the Flask App

Start the Flask app in your main terminal:

```bash
python app.py
```

This will start the server on `http://127.0.0.1:5000`.

---

## Usage

1. **Access the Dashboard**: Go to `http://127.0.0.1:5000` to view the email dashboard.
2. **Upload CSV or Connect Google Sheets**: Upload a CSV file or connect to a Google Sheets document for email personalization.
3. **Prompt Customization with LLM Integration**: Customize the email prompt template and use the Groq API to generate AI-based content.
4. **Sending Emails**: Use the uploaded data for personalization and click **Send Email**.
5. **Scheduling Emails**: Configure scheduling and throttling via **Schedule Email**.
6. **Real-Time Analytics**: Track email statuses (Sent, Pending, Failed) and LLM-generated content on the dashboard.

---

## LLM Integration (Groq API)

### Groq API Setup

1. Sign up at [Groq](https://groq.com/) and obtain an API key.
2. Add the API key to your environment variables (`GROQ_API_KEY`).

### Prompt Customization System

Define prompts with placeholders, such as `{Company Name}` or `{Location}`, which will be dynamically replaced by data from each row.

Example prompt:
```plaintext
"Dear {Company Name} team, we noticed that you have a strong presence in {Location}. Here’s a proposal for collaboration."
```

---

## Security Documentation

### OAuth2 Implementation for Secure Email Authentication

For enhanced security, OAuth2 can be used for Gmail and other services that support it.

### Secure Credential Storage Best Practices

1. **Environment Variables**: Store sensitive credentials in environment variables instead of hardcoding them in the code.
2. **Secrets Management**: Use secrets managers like AWS Secrets Manager or HashiCorp Vault for large applications.

---

## Enhanced Error Handling

The `send_custom_email` function includes specific error handling to manage email delivery errors gracefully.

```python
def send_custom_email(email_data):
    try:
        msg = MIMEText(email_data['content'])
        msg['Subject'] = email_data['subject']
        msg['From'] = email_data['sender']
        msg['To'] = email_data['recipient']

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_data['sender'], os.getenv("EMAIL_PASSWORD"))
            server.sendmail(email_data['sender'], email_data['recipient'], msg.as_string())

        return {"status": "Success", "message": "Email sent successfully"}
    except smtplib.SMTPAuthenticationError:
        return {"status": "Failed", "error": "Authentication error. Check email credentials or OAuth2 setup."}
    except smtplib.SMTPRecipientsRefused:
        return {"status": "Failed", "error": "Recipient address was refused by the server."}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}
```

---

## License

This project is for internal assessment purposes.

---
