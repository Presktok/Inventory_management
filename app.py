from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from backend.config.database import init_db
from backend.routes.inventory import inventory_bp
import os

# Load environment variables
load_dotenv()

# Create a global app instance
app = Flask(__name__,
            static_folder='frontend/static',
            template_folder='frontend/templates')

def create_app():
    # Configure app
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME', 'inventoryDB')
    
    # Enable CORS with development settings
    CORS(app, resources={
        r"/*": {  # Allow all routes during development
            "origins": "*",  # Allow all origins
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(inventory_bp, url_prefix='/api')
    
    return app

# Add route for the main pages
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
    
@app.route('/inventory')
def inventory():
    return render_template('inventory.html')
    
@app.route('/orders')
def orders():
    return render_template('orders.html')
    
@app.route('/routes')
def routes():
    return render_template('routes.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup logic here
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

# Add error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
