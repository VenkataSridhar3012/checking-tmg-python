from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config.from_pyfile('config.py')

# Initialize the database
db = SQLAlchemy(app)


# Import and register your routes and blueprints here
from app.main_routes import main_bp  # Import the main blueprint
from app.user_authentication.user_routes import user_bp  # Import your user_routes blueprint

# Register the routes and blueprints with the app
app.register_blueprint(main_bp)
app.register_blueprint(user_bp, url_prefix='/user')

