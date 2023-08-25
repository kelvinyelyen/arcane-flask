import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_session import Session
from datetime import datetime
from tempfile import mkdtemp
import smtplib
from email.mime.text import MIMEText
from html2text import html2text
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient

# Configure application
app = Flask(__name__)
app.secret_key = 'your-secret-key'
# Connect to MongoDB
app.config['MONGO_URI'] = os.environ.get('DB_URI')
mongo_client = MongoClient(app.config['MONGO_URI'])
db = mongo_client["arcane"]


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
MAILGUN_SMTP_SERVER = os.environ.get('MAILGUN_SMTP_SERVER')
MAILGUN_SMTP_USERNAME = os.environ.get('MAILGUN_SMTP_USERNAME')
MAILGUN_SMTP_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')

# Welcome emal config with mailgun smtp
def send_welcome_email(email, username):
    msg = MIMEText(
        f"Thank you for subscribing to my Newsletter! I'm are thrilled to have you.\n\nSincerely,\n{username.title()}")
    msg['Subject'] = f"{username.title()}"
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


# Custom filter to format date and time
@app.template_filter('datetime_format')
def datetime_format(value, format='%Y-%m-%d %H:%M:%S'):
    if value is None:
        return ""
    return value.strftime(format)

# Database Initialization
class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        db.users.insert_one(self.__dict__)
        
class Subscriber:
    def __init__(self, email, user_id):
        self.email = email
        self.user_id = user_id
        self.date_added = datetime.utcnow()

    # Methods for saving and querying data
    def save(self):
        db.subscribers.insert_one(self.__dict__)

    @staticmethod
    def find_by_user_id(user_id):
        return db.subscribers.find({"user_id": user_id})
    # ... Other methods ...


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Root route
@app.route("/")
def index():
    return render_template("index.html")


# Dashboard
@app.route("/dashboard")
def dashboard():
    username = session.get("username")
    email = session.get("email")

    # Retrieve the subscriber data from the session
    subscribers_data = session.get("subscribers_data")

    if not subscribers_data:
        print("No subscriber data found.")
        return redirect(url_for("subscribers"))

    return render_template("dashboard.html", username=username, email=email, num_subscribers=subscribers_data["num_subscribers"])


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Please enter your email and password.")
            return redirect(url_for("login"))

        user = db.users.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["_id"]
            session["username"] = user["username"]
            session["email"] = user["email"]
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.")
        return redirect(url_for("login"))

    return render_template("login.html")


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not email or not username or not password:
            flash("Please provide all required information")
            return redirect(url_for("register"))
        elif password != confirmation:
            flash("Passwords do not match")
            return redirect(url_for("register"))

        # Check if the username or email already exists in the database
        if db.users.find_one({"$or": [{"username": username}, {"email": email}]}):
            flash("Username or email already taken")
            return redirect(url_for("register"))

        # Create a new user
        new_user = User(username=username, email=email, password=password)
        new_user.save()

        return redirect(url_for("login"))

    else:
        return render_template("register.html")



# Logout
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/login")


# Subscribe
@app.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    if request.method == "GET":
        user_id = request.args.get("user_id")

        if not user_id:
            flash("Invalid subscription request")
            return redirect(url_for("subscribe"))

        # Retrieve the user details using the username
        user = db.users.find_one({"username": user_id})
        if not user:
            flash("Invalid subscription request")
            return redirect(url_for("subscribe"))

        return render_template("subscription.html", user_id=user_id)

    elif request.method == "POST":
        email = request.form.get("email")
        user_id = request.form.get("user_id")

        if not email or not user_id:
            flash("Invalid subscription request")
            return redirect(url_for("subscribe"))

        # Retrieve the user details using the username
        user = db.users.find_one({"username": user_id})
        if not user:
            flash("Invalid user")
            return redirect(url_for("subscribe"))

        # Check if the email already exists in the Subscriber collection
        existing_subscriber = db.subscribers.find_one(
            {"email": email, "user_id": user["_id"]})

        if existing_subscriber:
            flash("It seems you've already subscribed.")
            return render_template("subscription.html", user_id=user_id)

        subscriber = Subscriber(email=email, user_id=user["_id"])
        subscriber.save()

        send_welcome_email(email, user["username"])

        print("Thank you for subscribing!")
        return redirect(url_for("subscribed"))

    return render_template("subscription.html", user_id=user_id)


# Subscribers
@app.route("/subscribers")
def subscribers():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    user = db.users.find_one({"_id": user_id})

    subscribers = list(db.subscribers.find({"user_id": user_id}))

    num_subscribers = db.subscribers.count_documents({"user_id": user["_id"]})

    session["subscribers_data"] = {
        "num_subscribers": num_subscribers
    }

    return render_template("subscribers.html", user=user, subscribers=subscribers, num_subscribers=num_subscribers)


# Subscibed
@app.route("/subscribed", methods=["GET", "POST"])
def subscribed():
    if request.method == "GET":  # Access user_id from the URL parameter
        return render_template("subscribed.html")
    else:
        return render_template("subscribe.html")


# Compose
@app.route("/compose", methods=["GET", "POST"])
def compose():
    if request.method == "GET":
        user_id = session.get("user_id")
        if not user_id:
            flash("Please log in to access this page.")
            return redirect(url_for("login"))

        # Retrieve the user details using the user_id
        user = db.users.find_one({"_id": user_id})
        if not user:
            flash("Invalid user")
            return redirect(url_for("login"))

        return render_template("compose.html", user=user)

    elif request.method == "POST":
        user_id = session.get("user_id")
        if not user_id:
            flash("Please log in to access this page.")
            return redirect(url_for("login"))

        # Retrieve the user details using the user_id
        user = db.users.find_one({"_id": user_id})
        if not user:
            flash("Invalid user")
            return redirect(url_for("login"))

        # Get the message content from the form
        message_content = request.form.get("message_content")
        if not message_content:
            flash("Please enter a message.")
            return redirect(url_for("compose"))

        # Get all the subscribers of the user
        subscribers = db.subscribers.find({"user_id": user["_id"]})

        # Send the message to all the subscribers
        for subscriber in subscribers:
            send_email(subscriber.email, user.username, message_content)

        flash("Message sent successfully to all subscribers.")
        return redirect(url_for("dashboard"))


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



if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()
