from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_cors import CORS
from dotenv import load_dotenv
from backend.config.database import init_db
from backend.routes.inventory import inventory_bp
import os
import re
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import secrets
from pymongo import MongoClient
from datetime import timedelta

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Load environment variables
load_dotenv()

def create_app():
    # Create app instance
    app = Flask(__name__,
                static_folder='frontend/static',
                template_folder='frontend/templates')

    # Configure app
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME', 'inventoryDB')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7) # Session lasts 7 days
    
    # Enable CORS
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Initialize database
    try:
        init_db(app)
        print("MongoDB initialized successfully")
    except Exception as e:
        print(f"Error initializing MongoDB: {e}")
        raise e

    client = MongoClient(app.config['MONGO_URI'])
    db = client[app.config['MONGO_DBNAME']]
    users = db.users

    # Register blueprints
    app.register_blueprint(inventory_bp, url_prefix='/api')

    # Set Content Security Policy header
    @app.after_request
    def add_csp_header(response):
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com https://cdnjs.cloudflare.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https://images.unsplash.com *.tile.openstreetmap.org; "
            "connect-src 'self' http://localhost:5000 http://127.0.0.1:5000;"
        )
        response.headers['Content-Security-Policy'] = csp_policy
        return response

    # Password validation function
    def validate_password(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r"\d", password):
            return False, "Password must contain at least one number"
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"
        return True, "Password is valid"

    # Email validation function
    def validate_gmail(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
        return bool(re.match(pattern, email))

    # Define routes
    @app.route('/')
    def index():
        return render_template('dashboard.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            if not email or not password:
                flash('Please fill in all fields', 'error')
                return render_template('login.html')
            
            if not validate_gmail(email):
                flash('Please use a valid Gmail address', 'error')
                return render_template('login.html')
            
            remember_me = request.form.get('rememberMe')

            # Find user in database
            user = users.find_one({'email': email})
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = str(user['_id'])
                session['email'] = user['email']
                if remember_me:
                    session.permanent = True
                flash('Login successful!', 'success')

                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'error')
                return render_template('login.html')
                
        return render_template('login.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('index.html')

    @app.route('/inventory')
    @login_required
    def inventory():
        return render_template('inventory.html')

    @app.route('/orders')
    @login_required
    def orders():
        return render_template('orders.html')

    @app.route('/routes')
    @login_required
    def routes():
        return render_template('routes.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
            
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirmPassword')
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            
            if not all([email, password, confirm_password, first_name, last_name]):
                flash('Please fill in all fields', 'error')
                return render_template('signup.html')
            
            if not validate_gmail(email):
                flash('Please use a valid Gmail address', 'error')
                return render_template('signup.html')
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('signup.html')
            
            is_valid, message = validate_password(password)
            if not is_valid:
                flash(message, 'error')
                return render_template('signup.html')
            
            # Check if user already exists
            if users.find_one({'email': email}):
                flash('Email already registered', 'error')
                return render_template('signup.html')
            
            # Create new user
            hashed_password = generate_password_hash(password)
            user_data = {
                'email': email,
                'password': hashed_password,
                'first_name': first_name,
                'last_name': last_name
            }
            
            result = users.insert_one(user_data)
            
            if result.inserted_id:
                flash('Account created successfully! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error creating account. Please try again.', 'error')
                return render_template('signup.html')
                
        return render_template('signup.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out successfully', 'success')
        return redirect(url_for('index'))

    @app.route('/favicon.ico')
    def favicon():
        return '', 204

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        # Ensure the message is flashed only once
        if not session.get('404_flashed'):
            flash('The page you requested was not found.', 'error')
            session['404_flashed'] = True
        return redirect(url_for('index'))

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    print(f"Starting the Flask app on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)

