from app import app 
import resend
from email.mime.text import MIMEText
import smtplib
from html2text import html2text

MAILGUN_SMTP_SERVER = app.config.get('MAILGUN_SMTP_SERVER')
MAILGUN_SMTP_USERNAME = app.config.get('MAILGUN_SMTP_USERNAME')
MAILGUN_SMTP_PASSWORD = app.config.get('MAILGUN_SMTP_PASSWORD')

# RESEND_API_KEY = app.config.get('RESEND_API_KEY')

# Mailgun
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

# Resend
# def send_welcome_email(email, username):
#     params = {
#         "from": "your_email@example.com",
#         "to": email,
#         "subject": f"Welcome to the Newsletter, {username.title()}",
#         "html": f"Thank you for subscribing to my Newsletter! I'm thrilled to have you.<br><br>Sincerely,<br>{username.title()}",
#     }

#     try:
#         response = resend.Emails.send(params)
#         print(f"Welcome email sent successfully to {email}. Response: {response}")
#     except Exception as e:
#         print(f"Failed to send welcome email to {email}. Error: {str(e)}")


# def send_email(email, subject, content):
#     text_body = html2text(content)
#     params = {
#         "from": "your_email@example.com",
#         "to": email,
#         "subject": subject,
#         "html": content,
#     }

#     try:
#         response = resend.Emails.send(params)
#         print(f"Email sent successfully to {email}. Response: {response}")
#     except Exception as e:
#         print(f"Failed to send email to {email}. Error: {str(e)}")
