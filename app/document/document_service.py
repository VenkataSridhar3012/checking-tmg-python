import json
import re
from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
from sqlalchemy import func,extract
import os
import seaborn as sns 
import pandas as pd
from app.demand_planning.utill import melt_cols, make_DP_overview
from app import db  # Import your SQLAlchemy instance
from app.demand_planning.demand_model import DemandDataModel
from app.document.document_model import Document
from app.products.product_model import ProductDataModel


# save data from excel file 
def save_process_excel_file(file):
    try:
         # Check if a record for the current month and year already exists
        existing_record = Document.query.filter(
            extract('month', Document.createdAt) == func.extract('month', func.now()),
            extract('year', Document.createdAt) == func.extract('year', func.now())
        ).first()

        if existing_record:
        # A record for the current month already exists
        # You can raise an error or return a message as needed
         print("A record for the current month already exists.")
         response = "A record for the current month already exists."
         return response, 400, {'Content-Type': 'application/json'}
        
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
       
        response='successfully uploaded data '
        return response, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
def identify_files_data(file_paths):
    identified_data = {}

    for file_path in file_paths:
        # Read the file into a DataFrame
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            # Handle unsupported file types
            identified_data[file_path] = "unsupported_file_type"
            continue

        # Get the column names
        col_names = set(df.columns)

        # Define a regular expression pattern to match QTYITEMUNIT followed by a number
        qtyitemunit_pattern = re.compile(r'^QTYITEMUNIT(\d+)_$')

        # Check if the columns match any predefined patterns
        if "ITEMID" in col_names and any(qtyitemunit_pattern.match(col) for col in col_names):
            save_as = "customer_neutral_demand_forecast_fileData"
            
        elif col_names == {"ITEMID", "Menge", "Liefermonat"}:
            save_as = "customer_neutral_demand_orders_fileData"
        elif col_names == {"ITEMID", "CUSTACCOUNT", "DEFAULTAGREEMENTLINEEXPIRATIONDATE", "COMMITEDQUANTITY"}:
            save_as = "customer_specific_demand_project_fileData"
        elif col_names == {"ITEMID", "Menge", "CUSTACCOUNT", "Liefermonat"}:
            save_as = "customer_specific_demand_orders_fileData"
        elif col_names == {"ITEMID", "SALESPRICE", "LINEAMOUNT", "PACKAGEQTYRST", "PACKINGQTYRST"}:
            save_as = "pricing_fileData"
        elif col_names == {"ITEMID", "CUSTACCOUNT", "Backlog"}:
            save_as = "DP_backlog"
        elif col_names == {"ITEMID", "CUSTACCOUNT", "MONATID", "Menge"}:
            save_as = "demand_previous_year"
        else:
            save_as = "unknown_category"

        # Store the identified data in the variable
        identified_data[file_path] = save_as

    return identified_data

# {
#     "temp/01a_Forecast_without_Customers.xlsx": "customer_neutral_demand_forecast_fileData",
#     "temp/04_Daten_StdPreis_Berechnung.xlsx": "pricing_fileData",
#     "temp/05_DP_Product_Backlog.xlsx": "DP_backlog",
#     "temp/Kundendedizierter_Bedarf_Kaufverträge_neu.xlsx": "customer_specific_demand_project_fileData",
#     "temp/Open_Orders_neu.xlsx": "customer_specific_demand_orders_fileData",
#     "temp/Open_Orders_ohne_Kunden_neu.xlsx": "customer_neutral_demand_orders_fileData",
#     "temp/demand_prev_Year_mit Kunden_neu.xlsx": "demand_previous_year"
# }

