from flask import redirect, Blueprint, render_template, session, url_for
from app import app

@app.route("/dashboard")
def dashboard():
    username = session.get("username")
    email = session.get("email")

    subscribers_data = session.get("subscribers_data")

    if not subscribers_data:
        print("No subscriber data found.")
        return redirect(url_for("subscribers"))

    return render_template("dashboard.html", username=username, email=email, num_subscribers=subscribers_data["num_subscribers"])



