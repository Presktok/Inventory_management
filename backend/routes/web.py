import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def dashboard():
    return render_template('dashboard.html')  # Show your homepage first

@web_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([first_name, last_name, email, password]):
            flash("Missing required fields", "danger")
            return redirect(url_for('web.signup'))

        full_name = f"{first_name} {last_name}"

        db = current_app.db
        users_collection = db.users

        # Check if the user already exists
        if users_collection.find_one({"email": email}):
            flash("User  already exists", "danger")
            return redirect(url_for('web.signup'))

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Insert the new user
        users_collection.insert_one({
            "name": full_name,
            "email": email,
            "password": hashed_password
        })

        flash("Signup successful! You can now log in.", "success")
        return redirect(url_for('web.login'))  # Redirect after signup

    return render_template('signup.html')

@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db = current_app.db
        users_collection = db.users  # Make sure this collection is correct

        try:
            user = users_collection.find_one({"email": email})

            if user:
                if check_password_hash(user.get('password'), password):
                    session['user'] = {
                        "name": user.get("name"),
                        "email": user.get("email")
                    }
                    print("[DEBUG] Login successful.")
                    return redirect(url_for('web.index_page'))
                else:
                    flash("Invalid credentials. Please try again.", "danger")
                    print("[DEBUG] Incorrect password.")
            else:
                flash("Invalid credentials. Please try again.", "danger")
                print("[DEBUG] No user found with that email.")

        except Exception as e:
            flash("Something went wrong. Please try again.", "danger")
            print(f"[ERROR] Exception during login: {e}")

    return render_template('login.html')


@web_bp.route('/index')
def index_page():  # Renamed to avoid conflict
    return render_template('index.html')

@web_bp.route('/inventory')
def inventory():
    return render_template('inventory.html')

@web_bp.route('/order')
def orders():
    return render_template('order.html')

@web_bp.route('/routes')
def routes():
    return render_template('routes.html')

@web_bp.route('/prince')
def prince():
    return render_template('test.html')
