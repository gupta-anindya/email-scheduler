Here’s a detailed **README.md** to guide users through setup, configuration, and usage.

---

# Custom Email Sender for BreakoutAI

This project is a custom email-sending application with scheduling, throttling, and real-time tracking capabilities. It reads data from Google Sheets or CSV files, allows email account connections, and customizes and sends emails using dynamic fields. The project includes a real-time analytics dashboard for monitoring sent emails.

---

## Project Structure

```
email_sender/
├── app.py              # Main Flask app
├── email_sender.py     # Email sending functions
├── scheduler.py        # Scheduling and throttling
├── config.json         # Configuration for email settings and API keys
├── templates/
│   └── dashboard.html  # Dashboard for real-time tracking
└── README.md           # Project documentation
```

---

## Requirements

- Python 3.x
- [Flask](https://flask.palletsprojects.com/en/2.1.x/): `pip install Flask`
- [Celery](https://docs.celeryproject.org/en/stable/): `pip install celery`
- [Redis](https://redis.io/): for scheduling and throttling. Install via `redis-server`.
- [Pandas](https://pandas.pydata.org/): `pip install pandas`
- [smtplib](https://docs.python.org/3/library/smtplib.html): included in Python standard library.

---

## Setup and Configuration

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd email_sender
```

### Step 2: Configure `config.json`

In the `config.json` file, configure the SMTP settings for your email service provider. 

Example configuration for Gmail:
```json
{
  "email_sender": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 465,
    "email": "your-email@gmail.com",
    "password": "your-email-password"
  }
}
```

> **Note**: For Gmail, you may need to enable [App Passwords](https://support.google.com/accounts/answer/185833?hl=en) if two-factor authentication (2FA) is enabled.

### Step 3: Start Redis Server

Ensure Redis is running. Start Redis in a new terminal window:

```bash
redis-server
```

### Step 4: Start Celery Worker

Open another terminal and navigate to the project directory, then run:

```bash
celery -A scheduler worker --loglevel=info
```

### Step 5: Run the Flask App

Start the Flask app in your main terminal:

```bash
python app.py
```

This will start the server on `http://127.0.0.1:5000`.

---

## Usage

1. **Access the Dashboard**: Go to `http://127.0.0.1:5000` to view the email dashboard.
2. **Sending Emails**:
   - Enter the email data in the form fields provided.
   - Click **Send Email** to initiate sending.
3. **Scheduling Emails**:
   - Enter scheduling details and click **Schedule Email**.
4. **Real-Time Analytics**: The dashboard shows email statuses (Sent, Pending, Failed) and delivery information.

---

## Code Overview

### `app.py`

The main file for the Flask application. This handles routing for:
- Sending emails via `/send_email`
- Scheduling emails via `/schedule_email`

### `email_sender.py`

Contains functions for sending emails, including:
- `send_custom_email`: Uses SMTP to send emails based on data.
- `load_data`: Reads data from CSV or Google Sheets for email personalization.

### `scheduler.py`

Handles email scheduling and throttling using Celery and Redis. The `schedule_email` function accepts a delay parameter to control email dispatch times.

### `templates/dashboard.html`

The HTML front-end dashboard for email tracking. Provides AJAX functionality to fetch and update email statuses in real-time.

---

## Important Notes

- **SMTP Configuration**: Ensure the SMTP settings in `config.json` match your email provider’s specifications.
- **OAuth2**: If using a more secure email setup, consider OAuth2 for account connection.
- **Rate Limiting**: Celery and Redis manage email throttling. Configure these based on your email provider’s sending limits.

---
