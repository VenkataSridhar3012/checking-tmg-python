import json
from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
from sqlalchemy import func,extract
import os
import seaborn as sns 
from app.demand_planning.utill import melt_cols, make_DP_overview
from app import db  # Import your SQLAlchemy instance
from app.demand_planning.demand_model import DemandDataModel
from app.document.document_model import Document
from app.products.product_model import ProductDataModel


# save data from excel file 
def save_process_excel_file(file):
    try:
         # Check if a record for the current month and year already exists
        # existing_record = Document.query.filter(
        #     extract('month', Document.createdAt) == func.extract('month', func.now()),
        #     extract('year', Document.createdAt) == func.extract('year', func.now())
        # ).first()

        # if existing_record:
        # # A record for the current month already exists
        # # You can raise an error or return a message as needed
        #  print("A record for the current month already exists.")
        #  response = "A record for the current month already exists."
        #  return response, 400, {'Content-Type': 'application/json'}
        
        current_datetime = datetime.now()
        # Create a new Document instance
        new_document = Document(
            startdate= current_datetime,
            productionCapacity='some_value',
            demandId='demandtest1',
            demandFileKey=file.filename,
            productId="test",
        )

        # Add the new document to the database
        db.session.add(new_document)
        db.session.commit()
        # fetching demand names from file 
        dmd_names = pd.read_excel(file, sheet_name='name_map').head(6)
        dmd_names = dmd_names.set_index('tool').to_dict()['client']
        json_data_dmd_names = json.dumps(dmd_names)
        print(type(json_data_dmd_names))
    
        # creating demand_customer_neutral data from file 
        demand_customer_neutral = pd.read_excel(file, sheet_name = 'demand_customer_neutral')
        demand_customer_neutral = melt_cols(demand_customer_neutral, [f'dmd_type_{i}' for i in range(1,5)], ['demand', 'demand_type'], [dmd_names[i] for i in list(dmd_names.keys())[:5]])
        customer_neutral = demand_customer_neutral
        data_array = customer_neutral.to_dict(orient='records')
        for item in data_array:
         item['date'] = item['date'].strftime('%Y-%m-%d %H:%M:%S')
        print(type(data_array))
        
        # creating demand_customer_specific data
        demand_customer_specific = pd.read_excel(file, sheet_name = 'demand_customer_specific')
        demand_customer_specific = melt_cols(demand_customer_specific, [f'dmd_type_{i}' for i in range(4,6)], ['demand', 'demand_type'], [dmd_names[i] for i in list(dmd_names.keys())[3:5]])

        # TBD - how to handle Kaufverträge
        demand_customer_specific.drop(columns = ['Kaufverträge'], inplace = True)
        demand_customer_specific.head()
        customer_specific= demand_customer_specific.head()
        data_array2 = customer_specific.to_dict(orient='records')
        for item in data_array2:
         item['date'] = item['date'].strftime('%Y-%m-%d %H:%M:%S')
        print(type(data_array2))
        
        
        
        new_document2 = DemandDataModel(
            
            customer_specific=data_array2,
            demandFileKey=file.filename,
            customer_neutral=data_array,
            date=current_datetime,
            demandDataType=json_data_dmd_names
        )

        db.session.add(new_document2)
        db.session.commit()
        
        # saving product details 
        product_details = pd.read_excel(file, sheet_name = 'product_base_data')
        data_array3 = product_details.to_dict(orient='records')
        document_id = new_document.id
        new_records = []
        for obj in data_array3:
            new_record = ProductDataModel(
                productNumber=obj["product_no"],
                productName=obj["product_name"],
                productSegmaentNumber=obj["product_segment_no"],
                productSegmentName=obj["product_segment_name"],
                materialNumber=obj["material_no"],
                materialName=obj["material_name"],
                documentId=document_id,
                productFileKey="product_base_data"
            )
            new_records.append(new_record)
        
        db.session.add_all(new_records)
        db.session.commit()
        
        # print(data_array3)
        print(type(data_array3))
       
        # creating overview
        demand = pd.concat([demand_customer_specific, demand_customer_neutral])
        demand['demand_type'] = demand['demand_type'].replace({value: key for key, value in dmd_names.items()})
        demand['customer'].fillna('none', inplace=True)
        demand.head()
        
        
        # add product categories to demand

        product_base_data = pd.read_excel(file, sheet_name='product_base_data')
        product_base_data = product_base_data[['product_segment_no', 'product_no', 'material_no']]

        # map by product
        demand = demand.merge(product_base_data, on='product_no', how='left')
        demand.head()
        
        product_segment_no = '009292V238-0800402-1'
        product_no = '009292V238-0800402-1'
        material_no = '009292V238-0800402-1'
        
        colours = {'dark_grey': '#404040', 'blue': '#636efa', 'green': '#00cc96', 'dark_blue': '#06038D', 'pink': '#ff007f', 'light_grey' :	'#D3D3D3', 'lighter_grey': '#F2F2F2'}
        blues = sns.light_palette(colours['blue'], n_colors=6).as_hex()
        blues.reverse()
        greens = sns.light_palette(colours['green'], n_colors=6).as_hex()
        greens.reverse()
        
        DP_overview = make_DP_overview(product_segment_no = product_segment_no, product_no = product_no, material_no = material_no
        , demand = demand,dmd_names=dmd_names)
        
        
        
        print(DP_overview)
        response = demand.head()
        response = response.to_json(orient='records')
        return response, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
    
    
    
# def customer_specfic(file):
    try:
        
        
       
        
            
              
              
        
        # add product categories to demand

        product_base_data = pd.read_excel(file, sheet_name='product_base_data')
        product_base_data = product_base_data[['product_segment_no', 'product_no', 'material_no']]

        # map by product
        demand = demand.merge(product_base_data, on='product_no', how='left')
        demand.head()
        
        product_segment_no = '009292V238-0800402-1'
        product_no = '009292V238-0800402-1'
        material_no = '009292V238-0800402-1'
        
        colours = {'dark_grey': '#404040', 'blue': '#636efa', 'green': '#00cc96', 'dark_blue': '#06038D', 'pink': '#ff007f', 'light_grey' :	'#D3D3D3', 'lighter_grey': '#F2F2F2'}
        blues = sns.light_palette(colours['blue'], n_colors=6).as_hex()
        blues.reverse()
        greens = sns.light_palette(colours['green'], n_colors=6).as_hex()
        greens.reverse()
        
        DP_overview = make_DP_overview(product_segment_no = product_segment_no, product_no = product_no, material_no = material_no
        , demand = demand,dmd_names=dmd_names)
        
        
        
        print(DP_overview)
        response = demand.head()
        response = response.to_json(orient='records')
        return response, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        return jsonify({'error': str(e)}), 500