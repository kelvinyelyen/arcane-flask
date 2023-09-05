from flask import flash, Blueprint, redirect, render_template, request, session, url_for
from app import app
from app.models import User
from app import db
from werkzeug.security import check_password_hash

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
    session.clear()
    return redirect("/login")
