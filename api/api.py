from fastapi import FastAPI, File, UploadFile
from PIL import Image
import numpy as np
import io
from tensorflow import keras

# Inicializar la app de FastAPI
app = FastAPI()

# Cargar el modelo previamente entrenado
model = keras.models.load_model("model/digit_recognition_model.h5")

# Función para preprocesar la imagen
def preprocess_image(image):
    image = image.convert("L")  # Convertir a escala de grises
    image = image.resize((28, 28))  # Redimensionar la imagen a 28x28 píxeles
    image = np.array(image).astype("float32") / 255.0  # Normalizar la imagen
    image = np.expand_dims(image, axis=0)  # Añadir dimensión de batch
    image = np.expand_dims(image, axis=-1)  # Añadir canal
    print(f"Imagen preprocesada: {image.shape}")  # Imprimir la forma de la imagen preprocesada
    # Asegurarse de que la imagen tenga la forma correcta para el modelo
    if image.shape != (1, 28, 28, 1):
        raise ValueError("La imagen debe tener la forma (1, 28, 28, 1)")
    # Asegurarse de que la imagen tenga el tipo correcto
    if image.dtype != np.float32:
        raise ValueError("La imagen debe ser de tipo float32")
    
    # Devolver la imagen preprocesada
    return image

# Ruta para la predicción
@app.post("/predict/")
async def predict_digit(file: UploadFile = File(...)):
    # Leer la imagen cargada
    image = Image.open(io.BytesIO(await file.read()))
    # Preprocesar la imagen
    image = preprocess_image(image)
    # Realizar la predicción
    prediction = model.predict(image)
    digit = np.argmax(prediction)  # Obtener el dígito predicho
    return {"digit": int(digit)}  # Devolver la predicción en formato JSON


# Ruta para probar la API
@app.get("/hello/")
async def hello_world():
    return {"message": "Hello, World!"}
# Ruta para verificar el estado de la API
@app.get("/health/")
async def health_check():
    return {"status": "OK"}
# Ruta para obtener información sobre el modelo
@app.get("/model_info/")
async def model_info():
    return {
        "model": "Digit Recognition Model",
        "version": "1.0",
        "description": "A model to recognize handwritten digits from images."
    }