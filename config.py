import os
from tempfile import mkdtemp
from dotenv import load_dotenv

class Config:
    SECRET_KEY = 'your-secret-key'
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    
    # Load environment variables from .env file
    load_dotenv()
    MONGO_URI = os.environ.get('DB_URI')
    MAILGUN_SMTP_SERVER = os.environ.get('MAILGUN_SMTP_SERVER')
    MAILGUN_SMTP_USERNAME = os.environ.get('MAILGUN_SMTP_USERNAME')
    MAILGUN_SMTP_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
    RESEND_API_KEY = os.environ.get('RESEND_API_KEY')