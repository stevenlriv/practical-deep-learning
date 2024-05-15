from flask import Flask, request, jsonify, send_file
from fastai.vision.all import *

app = Flask(__name__)

# Load the trained model
model_path = './model.pkl'
learn = load_learner(model_path)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Check if an image file is present in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file found'}), 400

    image_file = request.files['image']

    # Save the uploaded image temporarily
    image_path = 'uploaded_image.jpg'
    image_file.save(image_path)

    # Prepare the image for prediction
    img = PILImage.create(image_path)

    # Make predictions
    pred_class, pred_idx, probs = learn.predict(img)

    # Prepare the response
    response = {
        'predicted_class': pred_class,
        'predicted_probabilities': probs.tolist()
    }

    # Remove the temporary image file
    os.remove(image_path)

    return jsonify(response)

if __name__ == '__main__':
    app.run()