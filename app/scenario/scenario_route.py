from flask import Blueprint, request, jsonify
from .scenario_service import sv_createScenario,sv_editScenario,sv_deleteScenario,get_scenario,get_scenarios
from flask_jwt_extended import jwt_required


# Create a blueprint for your routes
scenario_bp = Blueprint('scenario', __name__)

@scenario_bp.route('/create_scenario', methods=['POST'])
@jwt_required()
def create_scenario():
    data = request.get_json()

    return sv_createScenario(data)

@scenario_bp.route('/update_scenario/<string:id>', methods=['PUT'])
@jwt_required()
def update_scenario(id):
    data = request.get_json()
    
    return sv_editScenario(id,data)


@scenario_bp.route('/get_scenario/<string:id>', methods=['GET'])
@jwt_required()
def get_scenarioById(id):
    return get_scenario(id)

@scenario_bp.route('/get_scenarios/<string:id>', methods=['GET'])
@jwt_required()
def get_scenariosById(id):
    return get_scenarios(id)

@scenario_bp.route('/delete_scenario/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_scenario(id):
    return sv_deleteScenario(id)






