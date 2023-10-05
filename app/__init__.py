import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import yaml

# Initialize the Flask app
app = Flask(__name__)

# Load configuration based on environment
app_config = os.environ.get('APP_ENV', 'dev')  # Default to dev if not set
with open(f'config/config_{app_config}.yaml', 'r') as file:
    config_data = yaml.safe_load(file)
    app.config.update(config_data)

# Initialize the JWTManager with your Flask app
jwt = JWTManager(app)

# Initialize the database
db = SQLAlchemy(app)

# Ensure the 'temp' directory exists
os.makedirs('temp', exist_ok=True)

# Load Swagger configurations
app.config['SWAGGER'] = {
    'title': 'Your API',
    'uiversion': 3,
    'openapi': '3.0.2',
}
swagger = Swagger(app)


# Import and register your routes and blueprints here
from app.home_routes import main_bp  # Import the main blueprint
from app.user_authentication.user_routes import user_bp  # Import your user_routes blueprint
from app.demand_planning.demand_route import demandplanning_bp  # Import your user_routes blueprint
from app.document.document_route import document_bp  # Import your user_routes blueprint
from app.products.product_route import product_bp  # Import your user_routes blueprint
from app.scenario.scenario_route import scenario_bp  # Import your user_routes blueprint
from app.action_points.ap_route import actionPoint_bp  # Import your user_routes blueprint

# Register the routes and blueprints with the app
app.register_blueprint(main_bp)
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(demandplanning_bp, url_prefix='/api/demand')
app.register_blueprint(document_bp, url_prefix='/api/document')
app.register_blueprint(product_bp, url_prefix='/api/product')
app.register_blueprint(scenario_bp, url_prefix='/api/scenario')
app.register_blueprint(actionPoint_bp, url_prefix='/api/actionPoint')

