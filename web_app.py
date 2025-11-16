from flask import Flask, render_template, request, jsonify
import numpy as np
from keras.models import load_model
import cv2
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Load the model
MODEL = load_model("bestmodel.h5")

LABELS = {0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four", 
          5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the image data from the request
        data = request.json
        image_data = data['image']
        
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # Convert to grayscale numpy array
        img_array = np.array(image.convert('L'))
        
        # Find bounding box of the drawn digit (same as Pygame app)
        # Find all non-zero (white) pixels
        rows = np.any(img_array > 0, axis=1)
        cols = np.any(img_array > 0, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            raise ValueError("No digit detected. Please draw on the canvas.")
        
        # Get bounding box coordinates
        y_min, y_max = np.where(rows)[0][[0, -1]]
        x_min, x_max = np.where(cols)[0][[0, -1]]
        
        # Add boundary increment (same as Pygame: BOUNDARYINC = 5)
        BOUNDARYINC = 5
        height, width = img_array.shape
        rect_min_x = max(x_min - BOUNDARYINC, 0)
        rect_max_x = min(width, x_max + BOUNDARYINC + 1)
        rect_min_y = max(y_min - BOUNDARYINC, 0)
        rect_max_y = min(height, y_max + BOUNDARYINC + 1)
        
        # Crop to bounding box (same as Pygame app)
        img_cropped = img_array[rect_min_y:rect_max_y, rect_min_x:rect_max_x].astype(np.float32)
        
        # Preprocess the image (same as Pygame app)
        # Resize to 28x28
        image = cv2.resize(img_cropped, (28, 28))
        
        # Pad with 10 pixels on all sides
        image = np.pad(image, (10, 10), 'constant', constant_values=0)
        
        # Resize again to 28x28
        image = cv2.resize(image, (28, 28))
        
        # Normalize to [0, 1]
        image = image / 255.0
        
        # Reshape for model input
        image = image.reshape(1, 28, 28, 1)
        
        # Make prediction
        prediction = MODEL.predict(image, verbose=0)
        predicted_digit = int(np.argmax(prediction))
        confidence = float(np.max(prediction))
        
        return jsonify({
            'success': True,
            'digit': predicted_digit,
            'label': LABELS[predicted_digit],
            'confidence': round(confidence * 100, 2),
            'probabilities': {
                str(i): round(float(prediction[0][i]) * 100, 2) 
                for i in range(10)
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

