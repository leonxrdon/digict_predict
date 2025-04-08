# API de Reconocimiento de Dígitos

Este proyecto proporciona una aplicación web y una API para reconocer dígitos escritos a mano. Los usuarios pueden dibujar un dígito en un lienzo o cargar una imagen de un dígito, y la aplicación predecirá el dígito utilizando un modelo de aprendizaje automático preentrenado.

## Características

- **Interfaz Web**: Una interfaz fácil de usar para dibujar dígitos o cargar imágenes.
- **API**: Una API RESTful para el reconocimiento de dígitos.
- **Modelo**: Utiliza un modelo de TensorFlow/Keras entrenado en conjuntos de datos de dígitos escritos a mano.

## Requisitos

- Python 3.8 o superior
- Paquetes de Python requeridos (instalar con `requirements.txt`):
## Instalación

1. Clona el repositorio:
     ```bash
     git clone https://github.com/leonxrdon/digit_predict.git
     cd digit_predict
     ```

2. Crea un entorno virtual y actívalo:
     ```bash
     python -m venv venv
     venv\Scripts\activate  # En Windows
     source venv/bin/activate # En Linux
     ```

3. Instala las dependencias requeridas:
     ```bash
     pip install -r requirements.txt
     ```

4. Asegúrate de que el modelo preentrenado esté ubicado en `api/model.h5`.

## Ejecución del Proyecto

1. Inicia el servidor Flask:
     ```bash
     python app.py
     ```

2. Abre tu navegador y navega a:
     ```
     http://127.0.0.1:5003/
     ```
3. Dibuja el dígito y mira el resultado
   
![predict](https://github.com/user-attachments/assets/2b7a1e06-4634-48bb-b33f-befc02e064b0)

## Estructura del Proyecto

```
api/
├── app.py              # Lógica principal de la API
├── utils.py            # Funciones de apoyo
├── templates/          # Plantillas HTML para la interfaz web
│   └── index.html
├── static/             # Archivos estáticos (CSS, JS)
├── model.h5            # Archivo del modelo
├── README.md           # Documentación del proyecto
└── requirements.txt    # Dependencias de Python
notebook/
├── model.h5            # Archivo del modelo
├── numbers.ipynb       # Notebook de entrenamiento
README.md               # Información sobre el proyecto
```

## Características

- **Web Interface**: A user-friendly interface for drawing digits or uploading images.
- **API**: A RESTful API for digit recognition.
- **Model**: Uses a TensorFlow/Keras model trained on handwritten digit datasets.
