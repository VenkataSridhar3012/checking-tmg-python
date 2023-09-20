from flask import Blueprint, request, jsonify
from .overview import process_excel_file 

# Create a blueprint for your routes
overview_bp = Blueprint('overview', __name__)

@overview_bp.route('/overview', methods=['POST'])
def overview():
    # Check if a file was sent with the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
  
    # Check if the file has a valid filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file is an Excel file
    if not file.filename.endswith('.xlsx'):
        return jsonify({'error': 'Invalid file format. Only .xlsx files are allowed.'}), 400

    # Call the service function to process the file
    return process_excel_file(file)


