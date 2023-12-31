from flask import Blueprint, request, jsonify
from .overview import get_overivewData 
from .customer_neutral import get_customer_neutral_data 
from .customer_specfic import get_customer_specfic_data 

# Create a blueprint for your routes
demandplanning_bp = Blueprint('demandplanning', __name__)

@demandplanning_bp.route('/overview', methods=['GET'])
def overview():
    # Call the service function
    return get_overivewData()



@demandplanning_bp.route('/customer_specfic_data', methods=['GET'])
def customer_specfic_data():
    
    # Call the service function
    return get_customer_specfic_data()


@demandplanning_bp.route('/customer_neutral_data', methods=['GET'])
def customer_neutral_data():
    
    # Call the service function 
    return get_customer_neutral_data()


