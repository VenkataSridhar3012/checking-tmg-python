from flask import Flask, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful_swagger_2 import Api as SwaggerApi

# Initialize the Flask app
app = Flask(__name__)



# Initialize Swagger with host information
swagger = SwaggerApi(app, api_version='1.0', title='Your API Title', description='Your API Description', host='127.0.0.1:8081')

print(swagger)


# Load configuration from config.py
app.config.from_pyfile('config.py')

# Initialize the JWTManager with your Flask app
jwt = JWTManager(app)

# Initialize the database
db = SQLAlchemy(app)


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
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(demandplanning_bp, url_prefix='/demand')
app.register_blueprint(document_bp, url_prefix='/document')
app.register_blueprint(product_bp, url_prefix='/product')
app.register_blueprint(scenario_bp, url_prefix='/scenario')
app.register_blueprint(actionPoint_bp, url_prefix='/actionPoint')

