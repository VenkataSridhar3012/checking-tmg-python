from flask import Blueprint, request, jsonify
from .document_service import save_process_excel_file

# Create a blueprint for your routes
document_bp = Blueprint('document', __name__)


@document_bp.route('/uploadfile', methods=['POST'])
def uploadfile():
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
    return save_process_excel_file(file)

