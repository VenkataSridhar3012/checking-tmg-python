from flask import Blueprint, request, jsonify
from .product_service import get_products_details , get_productsIds_details
from flask_jwt_extended import jwt_required


# Create a blueprint for your routes
product_bp = Blueprint('product', __name__)

@product_bp.route('/getProduct', methods=['GET'])
@jwt_required()
def getProduts():
    return get_products_details()


@product_bp.route('/getProducts_with_ids', methods=['GET'])
@jwt_required()
def getProductsWithIds():
    # Get query parameters from the URL
    from_param = request.args.get('from')
    to_param = request.args.get('to')

    # Get JSON data from the request body
    data = request.get_json()

    # Retrieve the 'ids' list from the JSON data
    ids_to_retrieve = data.get('ids', [])

    # Use 'from_param' and 'to_param' directly in your function if needed
    return get_productsIds_details(ids_to_retrieve, from_param, to_param)




