from flask import Blueprint, request, jsonify
from .scenario_service import sv_createScenario,sv_editScenario,sv_deleteScenario


# Create a blueprint for your routes
scenario_bp = Blueprint('scenario', __name__)

@scenario_bp.route('/create_scenario', methods=['POST'])
def create_scenario():
    data = request.get_json()

    return sv_createScenario(data)

@scenario_bp.route('/update_scenario/<string:id>', methods=['PUT'])
def update_scenario(id):
    data = request.get_json()
    
    return sv_editScenario(id,data)

@scenario_bp.route('/delete_scenario/<string:id>', methods=['DELETE'])
def delete_scenario(id):
    return sv_deleteScenario(id)






