import requests

# Ruta de la API
url = "http://127.0.0.1:8000/predict/"

# Ruta de la imagen a enviar
image_path = "test/number.png" 

# Abrir la imagen en modo binario
with open(image_path, "rb") as image_file:
    files = {"file": image_file}
    
    # Realizar la solicitud POST a la API
    response = requests.post(url, files=files)

# Imprimir la respuesta de la API
if response.status_code == 200:
    result = response.json()
    print(f"Predicción del dígito: {result['digit']}")
else:
    print(f"Error al hacer la solicitud: {response.status_code}")
