from flask import jsonify
from datetime import datetime
from app.products.product_model import ProductDataModel
from sqlalchemy import and_


def get_products_details():
    try:
        # Get the current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Calculate the start and end date for the current month
        start_date = datetime(current_year, current_month, 1)
        end_date = (
            datetime(current_year, current_month + 1, 1)
            if current_month < 12
            else datetime(current_year + 1, 1, 1)
        )

        product_data = ProductDataModel.query.filter(
            and_(
                ProductDataModel.createdAt >= start_date,
                ProductDataModel.createdAt < end_date,
            )
        ).all()

        productdata_list = None

        if product_data:
            productdata_list = [
                {
                    "id": item.id,
                    "productNumber": item.productNumber,
                    "productName": item.productName,
                    "productSegmaentNumber": item.productSegmaentNumber,
                    "productSegmentName": item.productSegmentName,
                    "materialNumber": item.materialNumber,
                    "materialName": item.materialName,
                    "documentId": item.documentId,
                    "productFileKey": item.productFileKey,
                    "createdAt": item.createdAt,
                    "updatedAt": item.updatedAt,
                }
                for item in product_data
            ]

        else:
            return_msg = "No matching document found"
            return return_msg

        return productdata_list, 200, {"Content-Type": "application/json"}

    except Exception as e:
        return jsonify({"error": str(e)}), 500



def get_productsIds_details(ids):
    try:
        # Get the current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Calculate the start and end date for the current month
        start_date = datetime(current_year, current_month, 1)
        end_date = (
            datetime(current_year, current_month + 1, 1)
            if current_month < 12
            else datetime(current_year + 1, 1, 1)
        )

        # Replace this with your array of IDs
        ids_to_retrieve = ids
        # ids_to_retrieve = [1, 2, 3]  # Replace with your desired IDs

        product_data = ProductDataModel.query.filter(
            and_(
                ProductDataModel.createdAt >= start_date,
                ProductDataModel.createdAt < end_date,
                ProductDataModel.id.in_(ids_to_retrieve)  # Filter by IDs
            )
        ).all()

        productdata_list = None

        if product_data:
            productdata_list = [
                {
                    "id": item.id,
                    "productNumber": item.productNumber,
                    "productName": item.productName,
                    "productSegmaentNumber": item.productSegmaentNumber,
                    "productSegmentName": item.productSegmentName,
                    "materialNumber": item.materialNumber,
                    "materialName": item.materialName,
                    "documentId": item.documentId,
                    "productFileKey": item.productFileKey,
                    "createdAt": item.createdAt,
                    "updatedAt": item.updatedAt,
                }
                for item in product_data
            ]

        else:
            return_msg = "No matching document found"
            return return_msg

        return productdata_list, 200, {"Content-Type": "application/json"}

    except Exception as e:
        return jsonify({"error": str(e)}), 500
