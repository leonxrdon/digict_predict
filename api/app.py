import numpy as np
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import io
import os
from utils import preprocess_image


# Cargar el modelo entrenado
model = load_model('model.h5')

app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para predecir el dígito
@app.route('/predict', methods=['POST'])
def predict():
    # Obtener la imagen enviada desde el frontend
    img_data = request.files['image']
    
    # Leer la imagen y agregar un fondo blanco
    img = Image.open(img_data).convert("RGBA")
    white_background = Image.new("RGBA", img.size, "WHITE")
    img = Image.alpha_composite(white_background, img).convert("RGB")
    
    # Guardar la imagen original con fondo blanco para inspección (sobrescribir siempre)
    original_image_path = "static/tmp/original_image.png"
    img.save(original_image_path)
    print(f"Imagen original guardada en: {original_image_path}")
    
    # Convertir la imagen a bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')  # Convertir a bytes
    img_bytes = img_bytes.getvalue()
    
    # Preprocesar la imagen para detectar múltiples números
    processed_images, bounding_boxes = preprocess_image(img_bytes, detect_multiple=True)
    
    results = []
    for idx, img in enumerate(processed_images):
        # Realizar la predicción
        prediction = model.predict(img)
        percentages = [f"{p:.2%}" for p in prediction[0]]
        
        # Guardar la imagen procesada (sobrescribir siempre)
        processed_image_path = f"static/tmp/processed_image_{idx}.png"
        Image.fromarray((img[0] * 255).astype(np.uint8).squeeze(), mode='L').save(processed_image_path)
        
        results.append({
            "percentages": percentages,
            "processed_image": processed_image_path
        })
    
    return jsonify({"results": results, "original_image": original_image_path})

# Ruta para eliminar las imágenes generadas
@app.route('/clear-images', methods=['POST'])
def clear_images():
    image_paths = [
        "static/tmp/original_image.png",
        "static/tmp/processed_image_0.png",
        "static/tmp/processed_image_1.png",
        "static/tmp/processed_image_2.png",
        # Agrega más rutas si es necesario
    ]
    for path in image_paths:
        if os.path.exists(path):
            os.remove(path)
            print(f"Imagen eliminada: {path}")
    return jsonify({"message": "Imágenes eliminadas correctamente."})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5003)
