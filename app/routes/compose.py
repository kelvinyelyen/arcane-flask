"""
The `compose` function is a Flask route that allows a logged-in user to send a message to all their
subscribers.
:return: a response object that redirects the user to a different page. The specific page that the
user is redirected to depends on the logic in the function.
"""
from flask import flash, request, redirect, render_template, session, url_for
from app import app
from app.utils.email_utils import send_email
from app import db

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
