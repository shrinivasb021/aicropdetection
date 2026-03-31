from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load model
model = tf.keras.models.load_model("model/model.h5")

classes = [
    "Tomato Early Blight",
    "Potato Late Blight",
    "Corn Healthy",
    "Tomato Healthy"
]

def predict_disease(img_path):

    img = Image.open(img_path)
    img = img.resize((224, 224))

    img_array = np.array(img)
    img_array = img_array / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)

    class_index = np.argmax(prediction)

    confidence = round(
        float(np.max(prediction)) * 100,
        2
    )

    return classes[class_index], confidence


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"})

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    disease, confidence = predict_disease(filepath)

    return jsonify({
        "disease": disease,
        "confidence": confidence,
        "treatment":
        "Apply recommended pesticide and remove infected leaves."
    })


if __name__ == "__main__":
    app.run(debug=True)
