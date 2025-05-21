from flask import Flask
from flask_cors import CORS
from backend.config.database import init_db
from backend.routes.web import web_bp
from backend.routes.api import api_bp

# Create app with templates/static configured
app = Flask(__name__,
            template_folder="frontend/templates",
            static_folder="frontend/static")

CORS(app)  # Enable CORS on the correct app instance

# Configurations
app.config.from_object('backend.config.config.DevelopmentConfig')
app.secret_key = 'Mera_Namm_Prince_Kumar'

# Initialize MongoDB
init_db(app)

# Register Blueprints
app.register_blueprint(web_bp)       # No prefix for web routes
app.register_blueprint(api_bp, url_prefix='/api')  # Optional prefix for APIs

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
