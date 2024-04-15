from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import pandas as pd
import tensorflow as tf

app = Flask(__name__)

# Configure the maximum uploaded file size (e.g., 10MB)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Specify the path for uploaded files (avoiding execution directory for security)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv'}

# Load your pre-trained model
model = tf.keras.models.load_model('path_to_your_model/model.h5')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict():
    if 'transactionFile' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['transactionFile']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Assume the CSV doesn't have a header row, adjust as needed
        data = pd.read_csv(file_path, header=None)
        # Process data as necessary for the model
        # This might include scaling, reshaping, etc.
        
        # Example: predict the uploaded data
        prediction = model.predict(data)
        os.remove(file_path)  # Clean up after prediction

        # Interpret your model's prediction result
        result = "Fraud" if prediction[0] > 0.5 else "Not Fraud"
        return jsonify({'message': f'Transaction is {result}.'})

    return jsonify({'message': 'Invalid file type'}), 400

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists
    app.run(debug=True)
