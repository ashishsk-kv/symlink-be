from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from .model import extract_text_from_pdf

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Define a blueprint for the routes
ocr = Blueprint('ocr', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ocr.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "no file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "no selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        extracted_text = extract_text_from_pdf(file_path)
        
        return jsonify({"extracted_text": extracted_text})
    else:
        return jsonify({"error": "invalid file type."}), 400
