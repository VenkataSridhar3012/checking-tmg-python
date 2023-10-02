from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from .ap_service import sv_create_actionPoint,sv_editActionPoint,sv_deleteActionPoint,sv_getActionPoints,get_actionPpoints_BasedOnCondition


# Create a blueprint for your routes
actionPoint_bp = Blueprint('actionPoint', __name__)

@actionPoint_bp.route('/create_actionPoint/<string:id>', methods=['POST'])
@jwt_required()
def create_actionPoint(id):
    data = request.get_json()
    return sv_create_actionPoint(id,data)

@actionPoint_bp.route('/update_actionPoint/<string:id>', methods=['PUT'])
@jwt_required()
def update_actionPoint(id):
    data = request.get_json()
    return sv_editActionPoint(id,data)

@actionPoint_bp.route('/getAll_actionPoint/<string:id>', methods=['GET'])
@jwt_required()
def Get_actionPoint(id):
    scenarioId = id,
    return sv_getActionPoints(scenarioId)


# based on condition
@actionPoint_bp.route('/get_actionpointsByCondition/<string:id>', methods=['GET'])
@jwt_required()
def get_actionpoints(id):
    scenario_id = id,
    data = request.get_json()
    product_segments = data.get('product_segments', [])
    product_groups = data.get('product_groups', [])
    products = data.get('products', [])
    customer_name = data.get('customerName')
    return get_actionPpoints_BasedOnCondition(product_segments,product_groups,products,scenario_id,customer_name)



@actionPoint_bp.route('/delete_actionPoint/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_actionPoint(id):
    return sv_deleteActionPoint(id)






