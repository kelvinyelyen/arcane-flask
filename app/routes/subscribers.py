from flask import flash, request, redirect, render_template, session, url_for
from app import app
from app.models import Subscriber
from app.utils.email_utils import send_welcome_email
from app import db
from app.filters import datetime_format

# Subscibe
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
    if request.method == "GET": 
        return render_template("subscribed.html")
    else:
        return render_template("subscribe.html")


