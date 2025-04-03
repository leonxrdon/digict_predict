# Digit Recognition API

Este proyecto implementa un modelo de reconocimiento de dígitos utilizando **TensorFlow** y **FastAPI**. El modelo es capaz de predecir dígitos a partir de imágenes de la base de datos MNIST.

## Requisitos

Asegúrate de tener Python 3.8 o superior instalado en tu sistema. Luego, instala las dependencias necesarias con:

```bash
pip install -r requirements.txt
```
El archivo `requirements.txt` debe contener las librerías necesarias, como `tensorflow`, `fastapi`, `uvicorn`, `pillow`, entre otras.

## Ejecutando la API

Para iniciar la API y probar el modelo de predicción de dígitos, ejecuta el siguiente comando:
```bash
uvicorn api:app --reload
```

Este comando iniciará el servidor en el puerto 8000 por defecto. Ahora puedes acceder a la API en `http://127.0.0.1:8000`.

## Probar el Modelo

1. Coloca la imagen que deseas probar en la carpeta `test` (que debe contener imágenes para hacer las predicciones).
   
2. Para hacer una predicción utilizando el modelo, ejecuta el archivo `client.py`:
```bash
python client.py
```

El archivo `client.py` se encargará de enviar la imagen al endpoint de la API (`/predict/`) y te mostrará el dígito predicho por el modelo.

### Estructura de la Carpeta

- `api.py`: Código de la API con FastAPI para servir el modelo.
- `client.py`: Cliente para enviar una imagen y obtener la predicción.
- `test/`: Carpeta que contiene las imágenes que deseas probar.

## Ejemplo de Uso

Para probar la API con una imagen:

1. Coloca una imagen de un dígito dentro de la carpeta `test/`.
2. Ejecuta el `client.py` para obtener la predicción.

El modelo devolverá un JSON con el dígito predicho.

### Predicción

Cuando envíes una imagen a la API, el formato de respuesta será algo como:
```json
{ "digit": 5 }
```
Este valor corresponde al dígito que el modelo predijo a partir de la imagen enviada.