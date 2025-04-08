import cv2
import numpy as np
import matplotlib.pyplot as plt

background_threshold = 127.5  # Umbral para decidir si el fondo es claro u oscuro


def preprocess_image(image_bytes, detect_multiple=False):
    # Convertir los bytes de la imagen a un array de numpy
    image_array = np.frombuffer(image_bytes, np.uint8)
    img_original = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)
 
    if img_original is None:
        raise ValueError("No se pudo cargar la imagen correctamente.")
 
    print(f"Imagen cargada (Dimensiones originales: {img_original.shape})")
 
    # --- Decidir si invertir colores ---
    avg_intensity = np.mean(img_original)
    print(f"Intensidad promedio de la imagen original: {avg_intensity:.2f}")
 
    if avg_intensity > background_threshold:
        print(f"Fondo detectado como CLARO (promedio > {background_threshold}). Invirtiendo colores.")
        img_original = cv2.bitwise_not(img_original)
    else:
        print(f"Fondo detectado como OSCURO (promedio <= {background_threshold}). Usando colores originales.")
 
    if detect_multiple:
        # Detectar contornos para múltiples números
        _, thresh = cv2.threshold(img_original, 127, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        processed_images = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            digit = img_original[y:y+h, x:x+w]
            
            # Crear un lienzo cuadrado para mantener la proporción
            size = max(w, h)
            square_canvas = np.zeros((size, size), dtype=np.uint8)
            offset_x = (size - w) // 2
            offset_y = (size - h) // 2
            square_canvas[offset_y:offset_y+h, offset_x:offset_x+w] = digit
            
            # Redimensionar a 28x28 píxeles
            digit_resized = cv2.resize(square_canvas, (28, 28), interpolation=cv2.INTER_AREA)
            digit_resized = digit_resized / 255.0
            digit_resized = digit_resized.reshape(-1, 28, 28, 1)
            processed_images.append(digit_resized)
        
        return processed_images, contours
 
    # Procesar una sola imagen
    h, w = img_original.shape
    size = max(w, h)
    square_canvas = np.zeros((size, size), dtype=np.uint8)
    offset_x = (size - w) // 2
    offset_y = (size - h) // 2
    square_canvas[offset_y:offset_y+h, offset_x:offset_x+w] = img_original

    processed_image = cv2.resize(square_canvas, (28, 28), interpolation=cv2.INTER_AREA)
    processed_image = processed_image / 255.0
 
    # Guardar la imagen procesada para inspección
    save_path = "tmp/processed_image.png"
    cv2.imwrite(save_path, (processed_image * 255).astype(np.uint8))
    print(f"Imagen procesada guardada en: {save_path}")
 
    # Ajustar forma a (1, 28, 28, 1) para el modelo
    processed_image = processed_image.reshape(-1, 28, 28, 1)
 
    return [processed_image], None
