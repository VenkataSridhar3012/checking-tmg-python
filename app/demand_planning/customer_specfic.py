import json
from flask import Flask, jsonify,send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import and_
from datetime import datetime
from app.demand_planning.demand_model import DemandDataModel
from app.document.document_model import Document
from app.products.product_model import ProductDataModel
from .utill import melt_cols, make_DP_overview, make_DP_customer_specific
from plotly.io import to_json


def get_customer_specfic_data():
    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Calculate the start and end date for the current month
    start_date = datetime(current_year, current_month, 1)
    end_date = datetime(current_year, current_month + 1, 1) if current_month < 12 else datetime(current_year + 1, 1, 1)

    # Query the database to fetch records within the current month
    document = Document.query.filter(and_(Document.createdAt >= start_date, Document.createdAt < end_date)).first()
    demand_data = DemandDataModel.query.filter(and_(DemandDataModel.createdAt >= start_date, DemandDataModel.createdAt < end_date)).first()
    product_data = ProductDataModel.query.filter(and_(ProductDataModel.createdAt >= start_date, ProductDataModel.createdAt < end_date)).all()
    
    customer_specific=None
    customer_neutral=None
    demand_DataType=None
    productdata_list=None
    
    if demand_data and document and product_data:
    #  print(demand_data.id)  # Access the id attribute
    #  print('customer_specific',demand_data.customer_specific)
    #  print("customer_neutral",demand_data.customer_neutral)  # Access the enddate attribute
    #  print("customer_neutral",demand_data.demandDataType)  # Access the enddate attribute
     
     productdata_list =[{'id': item.id,
              'productNumber': item.productNumber,
              'productName': item.productName,
              'productSegmaentNumber': item.productSegmaentNumber,
              'productSegmentName': item.productSegmentName,
              'materialNumber': item.materialNumber,
              'materialName': item.materialName,
              'documentId': item.documentId,
              'productFileKey': item.productFileKey,
              'createdAt': item.createdAt,
              'updatedAt': item.updatedAt
              } for item in product_data]
     
     
     customer_specific= demand_data.customer_specific
     customer_neutral= demand_data.customer_neutral
     demand_DataType= json.loads(demand_data.demandDataType)
    else:
        return_msg = 'No matching document found'
        return return_msg
     
    
    # print(type(customer_specific))
    demand = pd.DataFrame(customer_specific)
    demand['demand_type'] = demand['demand_type'].replace({value: key for key, value in demand_DataType.items()})
    demand['customer'].fillna('none', inplace=True)
    demand.head()
    
    
    product_df = pd.DataFrame(productdata_list)
    product_df = product_df[['productSegmaentNumber', 'productNumber', 'materialNumber']]
    # map by product
    demand = demand.merge(product_df, left_on='product_no', right_on='productNumber', how='left')
    demand.head()
    # print(demand.head())
    customer = 'Hilti AG'
    # user will choose this
    product_segment_no = '009292V238-0800402-1'
    product_no = '009292V238-0800402-1'
    material_no = '009292V238-0800402-1'
    response = {
      'customer_specific': customer_specific,
      'customer_neutral': customer_neutral,
      'demand_DataType': demand_DataType,
      'productdata_list': productdata_list
      }
    
    graph_data=make_DP_customer_specific(customer,product_segment_no,product_no,material_no,demand_DataType,demand)
    
    graph_data = to_json(graph_data)
    
    return graph_data
    
    