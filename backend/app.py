import tempfile
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from ocr_utils import process_image, convert_numpy_to_native
from uuid import uuid4

app = Flask(__name__)
CORS(app)

# Use temp directory for Vercel deployment
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return "Backend is running"

@app.route('/parse', methods=['POST'])
def parse_info():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    filename = secure_filename(str(uuid4()) + "_" + file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        result = process_image(file_path)
        result = convert_numpy_to_native(result)  # Convert numpy types to native Python types
        os.remove(file_path)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)