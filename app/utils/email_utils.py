import smtplib
from email.mime.text import MIMEText
from html2text import html2text
from app import app 

# Access the environment variables
MAILGUN_SMTP_SERVER = app.config.get('MAILGUN_SMTP_SERVER')
MAILGUN_SMTP_USERNAME = app.config.get('MAILGUN_SMTP_USERNAME')
MAILGUN_SMTP_PASSWORD = app.config.get('MAILGUN_SMTP_PASSWORD')

# Welcome email config with mailgun smtp
def send_welcome_email(email, username):
    msg = MIMEText(
        f"Thank you for subscribing to my Newsletter! I'm thrilled to have you.\n\nSincerely,\n{username.title()}")
    msg['Subject'] = f"Welcome to the Newsletter, {username.title()}"
    msg['From'] = MAILGUN_SMTP_USERNAME
    msg['To'] = email

    try:
        s = smtplib.SMTP(MAILGUN_SMTP_SERVER, 587)
        s.login(MAILGUN_SMTP_USERNAME, MAILGUN_SMTP_PASSWORD)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
        print(f"Welcome email sent successfully to {email}.")
    except Exception as e:
        print(f"Failed to send welcome email to {email}.")
        print(str(e))

# Function to send an email to a subscriber
def send_email(email, subject, content):
    text_body = html2text(content)
    msg = MIMEText(text_body)
    msg['Subject'] = subject
    msg['From'] = MAILGUN_SMTP_USERNAME
    msg['To'] = email

    try:
        s = smtplib.SMTP(MAILGUN_SMTP_SERVER, 587)
        s.login(MAILGUN_SMTP_USERNAME, MAILGUN_SMTP_PASSWORD)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
        print(f"Email sent successfully to {email}.")
    except Exception as e:
        print(f"Failed to send email to {email}.")
        print(str(e))
