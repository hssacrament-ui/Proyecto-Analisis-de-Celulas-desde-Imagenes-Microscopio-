# -*- coding: utf-8 -*-
"""
Script Unificado: Procesamiento y conteo de células para múltiples imágenes.
Este script valida los requerimientos técnicos para todas las imágenes del dataset en un solo flujo.
"""

import cv2 # Importa OpenCV para lectura, conversión de color y dibujo
import numpy as np # Importa NumPy para operaciones matriciales
import matplotlib.pyplot as plt # Importa Matplotlib para generar los gráficos de salida
import cell_segmentation_lib as lib # Importa la librería personalizada con las funciones de procesamiento

# Configuración de imágenes y parámetros específicos para optimizar el conteo en cada una
dataset = [ # Define una lista de diccionarios con la configuración de cada imagen a procesar
    {'ruta': 'imagen1.png', 'gamma': 1.2, 'cutoff': 50, 'area': 5},   # Reducido para detectar células más pequeñas
    {'ruta': 'Imagen2.png', 'gamma': 1.5, 'cutoff': 45, 'area': 30},  # Aumentado para filtrar objetos pequeños
    {'ruta': 'Imagen3.png', 'gamma': 1.2, 'cutoff': 40, 'area': 15},
    {'ruta': 'Imagen4.png', 'gamma': 1.2, 'cutoff': 40, 'area': 0},  # Sin filtro de área para detectar incluso los objetos más pequeños
    {'ruta': 'Imagen5.png', 'gamma': 1.2, 'cutoff': 40, 'area': 30}, # Aumentado area para ignorar detritos pequeños
    {'ruta': 'Imagen6.png', 'gamma': 1.1, 'cutoff': 60, 'area': 25}, # Mayor cutoff para intentar separar células muy juntas
    {'ruta': 'Imagen7.png', 'gamma': 1.8, 'cutoff': 45, 'area': 20}, # Gamma alto para compensar la tinción de los núcleos
    {'ruta': 'Imagen8.png', 'gamma': 1.2, 'cutoff': 40, 'area': 20}, # Configuración estándar para buen contraste
    {'ruta': 'Imagen9.png', 'gamma': 1.3, 'cutoff': 45, 'area': 15}, # Ajuste fino para células aisladas
    {'ruta': 'Imagen10.png', 'gamma': 1.6, 'cutoff': 35, 'area': 50} # Menor cutoff y mayor area para células grandes y borrosas
]

print("Iniciando procesamiento unificado del dataset...\n") # Imprime mensaje de inicio en consola

for data in dataset: # Itera a través de cada elemento de configuración en el dataset
    ruta_imagen = data['ruta'] # Extrae la ruta del archivo de imagen
    img = cv2.imread(ruta_imagen) # Carga la imagen desde el disco usando OpenCV
    
    if img is None: # Valida si la imagen se cargó correctamente
        print(f"Error: No se encontró {ruta_imagen} en la carpeta. Saltando...") # Avisa si el archivo no existe
        continue # Salta a la siguiente iteración si no hay imagen
        
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convierte de BGR (OpenCV) a RGB (estándar para visualización)

    # 1. PREPROCESAMIENTO Y TRANSFORMACIÓN DE INTENSIDAD (Gamma)
    gray = lib.rgb_to_gray(img_rgb) # Convierte la imagen a escala de grises usando la función manual de la lib
    gray_gamma = lib.intensity_transform(gray, gamma=data['gamma']) # Aplica corrección gamma para mejorar el contraste

    # 2. FILTRADO ESPACIAL (Gaussiano) Y EN FRECUENCIA (FFT Low Pass)
    blur = lib.spatial_filter_gaussian(gray_gamma, size=5, sigma=1.0) # Aplica desenfoque gaussiano para reducir ruido de alta frecuencia
    frecuencia = lib.frequency_filter_lowpass(blur, cutoff=data['cutoff']) # Realiza filtrado pasa bajos en el dominio FFT

    # 3. DETECCIÓN DE BORDES (Sobel Manual) Y UMBRALIZACIÓN (Otsu Manual)
    bordes = lib.edge_detection_sobel(frecuencia) # Detecta bordes usando gradientes de Sobel implementados manualmente
    binaria = lib.otsu_threshold(frecuencia) # Convierte la imagen a blanco y negro puro usando el umbral óptimo de Otsu

    # 4. SEGMENTACIÓN POR REGIONES Y MÉTODO DE CONTEO FINAL
    total, info_celulas = lib.manual_labeling(binaria, min_area=data['area']) # Etiqueta objetos y cuenta cuántos cumplen el área mínima

    # Visualización de resultados con etiquetado automático
    conteo_vis = img_rgb.copy() # Crea una copia de la imagen original para dibujar sobre ella sin modificarla
    for i, celula in enumerate(info_celulas): # Recorre la información de cada célula detectada
        x1, y1, x2, y2 = celula['box'] # Extrae las coordenadas de la caja delimitadora
        cv2.rectangle(conteo_vis, (x1, y1), (x2, y2), (0, 255, 0), 2) # Dibuja un rectángulo verde alrededor de la célula
        cv2.putText(conteo_vis, str(i+1), (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1) # Escribe el número identificador

    print(f"Procesada: {ruta_imagen} | Células detectadas: {total}") # Imprime el resultado final del conteo por imagen

    # Mostramos un resumen visual por cada imagen
    plt.figure(figsize=(15, 10)) # Ajustamos el tamaño para una disposición de 2 filas
    plt.subplot(2,3,1), plt.imshow(img_rgb), plt.title(f'Original: {ruta_imagen}') # Muestra la imagen de entrada
    plt.subplot(2,3,2), plt.imshow(bordes, cmap='gray'), plt.title('Sobel (Manual)') # Muestra los bordes detectados
    plt.subplot(2,3,3), plt.imshow(binaria, cmap='gray'), plt.title('Segmentación (Otsu)') # Muestra el resultado de la binarización
    plt.subplot(2,3,4), plt.hist(frecuencia.ravel(), 256, [0,256], color='black'), plt.title('Histograma (Intensidad)') # Genera el histograma de frecuencias de gris
    plt.subplot(2,3,5), plt.imshow(conteo_vis), plt.title(f'Resultado: {total} células') # Muestra el conteo final visualizado
    plt.tight_layout() # Ajusta automáticamente los espacios entre las gráficas
    plt.show() # Despliega la ventana con todos los resultados

print("\nProcesamiento de todas las imágenes completado con éxito.") # Mensaje de finalización global