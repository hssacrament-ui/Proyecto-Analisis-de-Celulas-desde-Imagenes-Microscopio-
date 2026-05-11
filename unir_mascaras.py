import cv2 # Importa OpenCV para manejo de imágenes
import numpy as np # Importa NumPy para operaciones matriciales
import glob # Importa glob para buscar archivos por patrones (ej: *.png)
import os # Importa os para manipulación de rutas de archivos

# Definimos la ruta de la carpeta donde están las 13 imágenes
# Usamos una ruta relativa para que funcione en cualquier computadora al descargar el repo
folder_path = os.path.join(os.path.dirname(__file__), 'Masks de prueba 1') 

# Buscamos todas las imágenes (puedes cambiar .png por .jpg si es necesario)
image_files = glob.glob(os.path.join(folder_path, '*.png')) # Crea una lista con todos los archivos .png encontrados

if len(image_files) == 0: # Comprueba si la lista de archivos está vacía
    print(f"No se encontraron imágenes en la carpeta '{folder_path}'.") # Avisa al usuario
else:
    print(f"Se encontraron {len(image_files)} imágenes. Iniciando la unión...") # Indica progreso

    # Cargamos la primera imagen para inicializar el lienzo
    combined_mask = cv2.imread(image_files[0], cv2.IMREAD_GRAYSCALE) # Lee la primera máscara como base de unión

    if combined_mask is None: # Valida que la carga de la primera imagen fue exitosa
        print("Error al leer la primera imagen.") # Avisa del error
    else:
        # Iteramos sobre el resto de las imágenes
        for i in range(1, len(image_files)): # Empieza desde el segundo elemento hasta el final
            mask = cv2.imread(image_files[i], cv2.IMREAD_GRAYSCALE) # Carga la máscara actual en gris
            
            if mask is not None: # Verifica que la imagen se cargó
                # Unimos las máscaras usando un OR bitwise (si un píxel es blanco en cualquiera, será blanco en el final)
                combined_mask = cv2.bitwise_or(combined_mask, mask) # Realiza la unión lógica de píxeles activos
            else:
                print(f"No se pudo cargar la imagen: {image_files[i]}") # Avisa si un archivo falló

        # Guardamos el resultado final
        output_path = os.path.join(folder_path, 'mascara_final_unida.png') # Define el nombre del archivo de salida
        cv2.imwrite(output_path, combined_mask) # Guarda la matriz resultante como imagen física
        
        print(f"¡Hecho! La imagen combinada se ha guardado en: {output_path}") # Confirma el guardado
        cv2.imshow('Mascara Unida', combined_mask) # Muestra la ventana con el resultado visual
        cv2.waitKey(0) # Espera a que el usuario presione una tecla
        cv2.destroyAllWindows() # Cierra las ventanas abiertas de OpenCV
