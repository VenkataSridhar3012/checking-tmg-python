from flask import Blueprint, request, jsonify
from .product_service import get_products_details , get_productsIds_details


# Create a blueprint for your routes
product_bp = Blueprint('product', __name__)

@product_bp.route('/getProduct', methods=['GET'])
def getProduts():
   
    return get_products_details()


@product_bp.route('/getProducts_with_ids', methods=['GET'])
def getProduts_ids():
    
    data = request.get_json()  # Get JSON data from the request body
    ids_to_retrieve = data.get('ids', [])  # Retrieve the 'ids' list from the JSON data
    return get_productsIds_details(ids_to_retrieve)




