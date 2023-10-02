import os
from flask import Blueprint, request, jsonify
from .document_service import save_process_excel_file,identify_files_data
from flask_jwt_extended import jwt_required

# Create a blueprint for your routes
document_bp = Blueprint('document', __name__)


@document_bp.route('/uploadfile', methods=['POST'])
@jwt_required()
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




@document_bp.route('/uploadfiles', methods=['POST'])
def identify_files():
    files = request.files.getlist('files')

    if not files:
        return jsonify({'error': 'No files provided'}), 400

    file_paths = []
    for file in files:
        # Save the file temporarily (you might want to handle file storage differently)
        file_path = f"temp/{file.filename}"
        file.save(file_path)
        file_paths.append(file_path)

    identified_data = identify_files_data(file_paths)

    # Cleanup: Remove the temporary files
    for file_path in file_paths:
        os.remove(file_path)

    return jsonify(identified_data)

