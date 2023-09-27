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

        
        target_key = 'productSegmaentNumber'
        unique_values = set()
        for d in productdata_list:
         if target_key in d:
        # Add the value to the set to ensure uniqueness
            unique_values.add(d[target_key]) 
        unique_values_list = list(unique_values)
      
        response={
            'productSegmaentNumber':unique_values_list
        }

        return response, 200, {"Content-Type": "application/json"}

    except Exception as e:
        return jsonify({"error": str(e)}), 500



def get_productsIds_details(ids,column_name1,column_name2):
    try:
       
        # Replace this with your array of IDs
        values_to_filter = ids
        # ids_to_retrieve = [1, 2, 3]  # Replace with your desired IDs
        # Get the column dynamically using getattr
        filter_dict = {}
        column = getattr(ProductDataModel, column_name1)

        filter_dict[column] = values_to_filter

        # Now, you can use this filter_dict in your query
        product_data = ProductDataModel.query.filter(
            and_(
                *[
                    column.in_(values)  # Unpack values list for the column
                    for column, values in filter_dict.items()
                ]
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
        
        
       
        target_key = column_name2
        unique_values = set()
        for d in productdata_list:
         if target_key in d:
        # Add the value to the set to ensure uniqueness
            unique_values.add(d[target_key])
        unique_values_list = list(unique_values)
      
        response={
           column_name2:unique_values_list
        }

        return response, 200, {"Content-Type": "application/json"}

    except Exception as e:
        return jsonify({"error": str(e)}), 500
