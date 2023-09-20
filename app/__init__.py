from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialize the Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config.from_pyfile('config.py')

# Initialize the JWTManager with your Flask app
jwt = JWTManager(app)

# Initialize the database
db = SQLAlchemy(app)


# Import and register your routes and blueprints here
from app.main_routes import main_bp  # Import the main blueprint
from app.user_authentication.user_routes import user_bp  # Import your user_routes blueprint
from app.demand_planning.demand_route import overview_bp  # Import your user_routes blueprint
from app.document.document_route import document_bp  # Import your user_routes blueprint

# Register the routes and blueprints with the app
app.register_blueprint(main_bp)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(overview_bp, url_prefix='/demand')
app.register_blueprint(document_bp, url_prefix='/document')

