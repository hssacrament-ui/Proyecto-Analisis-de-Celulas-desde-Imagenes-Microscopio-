# -*- coding: utf-8 -*-
"""Librería personalizada para procesamiento y conteo de células."""

import numpy as np # Importa NumPy para el manejo de matrices y arreglos numéricos
from scipy import signal # Importa el módulo signal para operaciones de convolución
from scipy.ndimage import label # Importa la función de etiquetado de objetos en imágenes binarias

def rgb_to_gray(img_rgb):
    """Conversión manual usando pesos estándar de luminancia."""
    return np.dot(img_rgb[...,:3], [0.2989, 0.5870, 0.1140]).astype(np.uint8) # Aplica producto punto entre los canales RGB y los pesos de luminancia para obtener la escala de grises

def intensity_transform(image, gamma=1.0):
    """Transformación de intensidad: Corrección Gamma."""
    invGamma = 1.0 / gamma # Calcula el inverso del valor gamma para la corrección
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8") # Crea una tabla de búsqueda (LUT) con los valores mapeados según la potencia gamma
    return table[image] # Aplica la tabla de búsqueda a la imagen de entrada para ajustar el contraste

def spatial_filter_gaussian(image, size=5, sigma=1.0):
    """Filtrado espacial: Implementación de desenfoque gaussiano."""
    x, y = np.mgrid[-size//2 + 1:size//2 + 1, -size//2 + 1:size//2 + 1] # Crea una rejilla de coordenadas centrada en cero según el tamaño del kernel
    g = np.exp(-((x**2 + y**2)/(2.0*sigma**2))) # Aplica la fórmula de la función gaussiana en 2D
    kernel = g / g.sum() # Normaliza el kernel para que la suma de sus elementos sea 1
    return signal.convolve2d(image, kernel, mode='same').astype(np.uint8) # Realiza la convolución de la imagen con el kernel gaussiano para suavizarla

def frequency_filter_lowpass(image, cutoff=30):
    """Filtrado en frecuencia: Filtro Ideal Pasa Bajos usando FFT."""
    f = np.fft.fft2(image) # Transforma la imagen del dominio espacial al dominio de la frecuencia (FFT)
    fshift = np.fft.fftshift(f) # Desplaza el componente de frecuencia cero (DC) al centro del espectro
    rows, cols = image.shape # Obtiene las dimensiones de la imagen (filas y columnas)
    crow, ccol = rows // 2, cols // 2 # Calcula el centro de la imagen para posicionar la máscara
    
    mask = np.zeros((rows, cols), np.uint8) # Inicializa una máscara negra (ceros) del tamaño de la imagen
    center = [crow, ccol] # Define las coordenadas centrales
    x, y = np.ogrid[:rows, :cols] # Crea rejillas vectorizadas para cálculos de distancia
    mask_area = (x - center[0])**2 + (y - center[1])**2 <= cutoff**2 # Define un círculo de radio 'cutoff' (frecuencia de corte)
    mask[mask_area] = 1 # Rellena el círculo de la máscara con blanco (unos)
    
    fshift = fshift * mask # Aplica la máscara al espectro de frecuencias (multiplicación punto a punto)
    f_ishift = np.fft.ifftshift(fshift) # Deshace el desplazamiento del centro
    img_back = np.fft.ifft2(f_ishift) # Aplica la transformada inversa de Fourier para volver al dominio espacial
    return np.abs(img_back).astype(np.uint8) # Retorna la magnitud del resultado convertido a 8 bits

def point_detection(image, threshold=150):
    """Detección de puntos usando el operador Laplaciano manual."""
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32) # Define un kernel Laplaciano para detectar cambios rápidos de intensidad
    laplacian = signal.convolve2d(image, kernel, mode='same') # Aplica convolución para resaltar puntos y bordes
    points = np.abs(laplacian) > threshold # Identifica los píxeles donde la respuesta del Laplaciano supera el umbral
    return points.astype(np.uint8) * 255 # Convierte la máscara booleana en una imagen binaria de 0 y 255

def hough_lines_manual(edge_image, threshold=50):
    """Transformada de Hough para líneas (implementación simplificada)."""
    rows, cols = edge_image.shape # Obtiene dimensiones de la imagen de bordes
    diag_len = int(np.ceil(np.sqrt(rows**2 + cols**2))) # Calcula la diagonal máxima para el rango de Rho
    rhos = np.linspace(-diag_len, diag_len, diag_len * 2) # Genera el vector de valores posibles para Rho
    thetas = np.deg2rad(np.arange(-90.0, 90.0)) # Genera el vector de ángulos Theta en radianes
    
    accumulator = np.zeros((len(rhos), len(thetas)), dtype=np.uint64) # Crea la matriz acumuladora para el espacio de parámetros
    y_idxs, x_idxs = np.where(edge_image > 0) # Obtiene las coordenadas de los píxeles que pertenecen a un borde
    
    for i in range(len(x_idxs)): # Itera sobre cada píxel de borde
        x, y = x_idxs[i], y_idxs[i] # Extrae coordenadas x, y
        for t_idx in range(len(thetas)): # Itera sobre cada posible ángulo
            rho = int(x * np.cos(thetas[t_idx]) + y * np.sin(thetas[t_idx])) + diag_len # Calcula Rho según la ecuación de la línea
            accumulator[rho, t_idx] += 1 # Incrementa el voto en el acumulador para esa combinación Rho/Theta
            
    return np.where(accumulator > threshold) # Retorna los índices donde el número de votos supera el umbral

def edge_detection_sobel(image):
    """Detección de bordes: Sobel manual."""
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32) # Define el kernel de Sobel para gradientes horizontales
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=np.float32) # Define el kernel de Sobel para gradientes verticales
    Ix = signal.convolve2d(image, Kx, mode='same') # Calcula el gradiente en X mediante convolución
    Iy = signal.convolve2d(image, Ky, mode='same') # Calcula el gradiente en Y mediante convolución
    mag = np.hypot(Ix, Iy) # Calcula la magnitud del gradiente combinando Ix e Iy (raíz de cuadrados)
    mag *= 255.0 / mag.max() # Normaliza la magnitud al rango [0, 255]
    return mag.astype(np.uint8) # Retorna la imagen de bordes en formato de 8 bits

def hough_circles_manual(edge_image, min_radius, max_radius, threshold):
    """
    Transformada de Hough para círculos programada manualmente.
    Retorna centros (x, y) y radios de los círculos detectados.
    """
    rows, cols = edge_image.shape # Obtiene las dimensiones de la imagen
    acc = {} # Crea un diccionario para actuar como acumulador 3D (a, b, r) disperso
    
    y_idxs, x_idxs = np.where(edge_image > 0) # Obtiene los puntos de interés (bordes)
    
    for i in range(len(x_idxs)): # Itera sobre cada punto de borde
        x = x_idxs[i] # Coordenada X del píxel de borde
        y = y_idxs[i] # Coordenada Y del píxel de borde
        
        for r in range(min_radius, max_radius + 1, 2): # Itera por el rango de radios permitidos (paso de 2 para velocidad)
            for theta in range(0, 360, 10): # Itera sobre ángulos de 0 a 360 (paso de 10 para velocidad)
                a = int(x - r * np.cos(np.radians(theta))) # Calcula la posible coordenada X del centro del círculo
                b = int(y - r * np.sin(np.radians(theta))) # Calcula la posible coordenada Y del centro del círculo
                
                if 0 <= a < cols and 0 <= b < rows: # Verifica si el centro calculado está dentro de los límites de la imagen
                    acc[(a, b, r)] = acc.get((a, b, r), 0) + 1 # Incrementa el voto para ese centro y radio
    
    circles = [] # Lista para almacenar círculos detectados
    for key, count in acc.items(): # Itera por el acumulador
        if count > threshold: # Si el número de votos supera el umbral establecido
            circles.append(key) # Añade la tupla (a, b, r) a la lista de resultados
            
    return circles # Retorna la lista de círculos encontrados

def otsu_threshold(image):
    """Algoritmo de umbralización de Otsu programado manualmente."""
    hist, bins = np.histogram(image.ravel(), 256, [0,256]) # Calcula el histograma de la imagen
    prob = hist / hist.sum() # Calcula las probabilidades de cada nivel de gris
    
    best_thresh = 0 # Variable para almacenar el mejor umbral encontrado
    max_variance = 0 # Almacena la varianza máxima entre clases
    
    for t in range(1, 256): # Itera por todos los posibles umbrales (niveles de gris)
        w0 = np.sum(prob[:t]) # Peso de la clase 1 (fondo)
        w1 = np.sum(prob[t:]) # Peso de la clase 2 (objetos)
        if w0 == 0 or w1 == 0: continue # Evita división por cero si una clase está vacía
        
        m0 = np.sum(np.arange(t) * prob[:t]) / w0 # Media de intensidad de la clase 1
        m1 = np.sum(np.arange(t, 256) * prob[t:]) / w1 # Media de intensidad de la clase 2
        
        variance = w0 * w1 * ((m0 - m1) ** 2) # Calcula la varianza entre clases de Otsu
        if variance > max_variance: # Busca maximizar esta varianza
            max_variance = variance # Actualiza la varianza máxima
            best_thresh = t # Actualiza el mejor umbral
            
    return (image > best_thresh).astype(np.uint8) * 255 # Retorna la imagen binarizada usando el umbral óptimo

def manual_labeling(binary_image, min_area=40):
    """Algoritmo de segmentación y conteo final (Etiquetado de componentes)."""
    from scipy.ndimage import label # Importa la función de etiquetado (redundante pero asegura alcance)
    if binary_image is None or np.max(binary_image) == 0: # Verifica si la imagen está vacía
        return 0, [] # Retorna conteo cero y lista vacía

    labeled_array, num_features = label(binary_image > 0) # Etiqueta cada isla de píxeles blancos con un número único
    
    final_count = 0 # Inicializa el contador de células válidas
    stats = [] # Lista para almacenar estadísticas (cajas, áreas) de cada célula
    for i in range(1, num_features + 1): # Itera sobre cada objeto detectado (del 1 al total de features)
        area = np.sum(labeled_array == i) # Calcula el área sumando los píxeles con la etiqueta actual
        if area >= min_area: # Filtra objetos que son demasiado pequeños para ser células (ruido)
            final_count += 1 # Incrementa el conteo final
            pos = np.where(labeled_array == i) # Obtiene las coordenadas de todos los píxeles del objeto
            stats.append({ # Almacena la caja delimitadora (min_x, min_y, max_x, max_y) y su área
                'box': (np.min(pos[1]), np.min(pos[0]), np.max(pos[1]), np.max(pos[0])),
                'area': area
            })
    return final_count, stats # Retorna el número total de células y sus detalles