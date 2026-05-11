# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 08:35:31 2026

@author: Carlos
"""

# ============================================================
# Segmentación y detección de características con OpenCV
# Temas:
# 1. Derivadas y gradiente
# 2. Sobel, Prewitt y Laplaciano
# 3. Canny
# 4. Umbralización y segmentación
# 5. Harris
# ============================================================

import cv2 # Importa OpenCV
import numpy as np # Importa NumPy
import matplotlib.pyplot as plt # Importa Matplotlib para gráficas
from scipy import signal # Importa procesamiento de señales (convolución)
from skimage import data # Importa datasets de ejemplo (monedas, etc.)

#%%
# CREAMOS IMAGEN DE PRUEBA SINTÉTICA
img_rgb = np.zeros((400, 500, 3), dtype=np.uint8) # Crea un lienzo negro de 400x500 RGB
cv2.circle(img_rgb, (120, 120), 60, (50, 50, 15), -1) # Dibuja un círculo relleno
cv2.circle(img_rgb, (260, 130), 55, (150, 255, 130), -1) # Dibuja otro círculo relleno
cv2.rectangle(img_rgb, (330, 250), (460, 340), (100, 100, 255), -1) # Dibuja un rectángulo azul
cv2.line(img_rgb, (40, 330), (220, 260), (100, 255, 255), 5) # Dibuja una línea amarilla

gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) # Convierte la imagen sintética a grises
plt.figure(1) # Crea figura 1
plt.subplot(1,2,1), plt.imshow(img_rgb) # Muestra imagen color
plt.subplot(1,2,2), plt.imshow(gray, cmap='gray') # Muestra imagen gris

#%%
#DERIVADAS Y GRADIENTE
#Derivadas
Hx = np.array([[0.5,0,-0.5]])
dx = signal.convolve2d(gray, Hx, mode='same')

Hy = Hx.T
dy = signal.convolve2d(gray, Hy, mode='same')

#magnitud del gradiente
grad = np.sqrt(dx**2 + dy**2)
#fase del gradiente
phase = np.arctan2(dy.copy(),dx.copy())
#Gráficas
plt.figure(2)
plt.subplot(2,2,1), plt.imshow(gray, cmap='gray'), plt.title('Original')
plt.subplot(2,2,2), plt.imshow(dx, cmap='gray'), plt.title('1st Derivada en X')
plt.subplot(2,2,3), plt.imshow(dy, cmap='gray'), plt.title('1st Derivada en Y')
plt.subplot(2,2,4), plt.imshow(grad, cmap='gray'), plt.title('Magnitud del gradiente')

#%%
# SOBEL, PREWITT Y LAPLACIANO
# Sobel
kernel_sx = np.array([[-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1]], dtype=np.float32)

kernel_sy = np.array([[ 1,  2,  1],
                      [ 0,  0,  0],
                      [-1, -2, -1]], dtype=np.float32)

edges_sx = signal.convolve2d(gray, kernel_sx, mode ='same')
edges_sy = signal.convolve2d(gray, kernel_sy, mode ='same')
sobel = cv2.magnitude(edges_sx, edges_sy)
#Graficas
plt.figure(3)
plt.subplot(1,2,1), plt.imshow(gray, cmap='gray'), plt.title('Imagen original')
plt.subplot(1,2,2), plt.imshow(sobel, cmap='gray'), plt.title('Sobel')


# Prewitt 
kernel_px = np.array([[-1, 0, 1],
                      [-1, 0, 1],
                      [-1, 0, 1]], dtype=np.float32)

kernel_py = np.array([[ 1,  1,  1],
                      [ 0,  0,  0],
                      [-1, -1, -1]], dtype=np.float32)

edges_px = signal.convolve2d(gray, kernel_px, mode ='same')
edges_py = signal.convolve2d(gray, kernel_py, mode ='same')
prewitt = cv2.magnitude(edges_px, edges_py)
#graficas
plt.figure(4)
plt.subplot(1,2,1), plt.imshow(gray, cmap='gray'), plt.title('Imagen original')
plt.subplot(1,2,2), plt.imshow(prewitt, cmap='gray'), plt.title('Prewitt')


# Laplaciano
laplaciano1 = np.array([[0, 1, 0],
                        [1,-4, 1],
                        [0, 1, 0]])

laplaciano2 = np.array([[1, 1, 1],
                        [1,-8, 1],
                        [1, 1, 1]])

edges1 = signal.convolve2d(gray, laplaciano1, mode ='same')
edges2 = signal.convolve2d(gray, laplaciano2, mode ='same')

#Graficas
plt.figure(5)
plt.subplot(1,3,1), plt.imshow(gray, cmap='gray'), plt.title('Imagen original')
plt.subplot(1,3,2), plt.imshow(edges1, cmap='gray'), plt.title('Laplaciano')
plt.subplot(1,3,3), plt.imshow(edges2, cmap='gray'), plt.title('Laplaciano C/diagonales')

#%%
# CANNY

blur = cv2.GaussianBlur(gray, (5, 5), 1.2)
edges_canny = cv2.Canny(blur,50,150) 
plt.figure(6)
plt.imshow(edges_canny, cmap='gray'), plt.title('Detector Canny')

#%%
# UMBRALIZACIÓN
# Global
th_global = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)

plt.figure(7)
plt.imshow(th_global[1], cmap='gray'), plt.title('Umbral binario')

#Otsu

plt.figure(10)
plt.hist(gray.ravel(), bins=50, range=(0, 255))
th_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
plt.figure(8)
plt.imshow(th_otsu[1], cmap='gray'), plt.title('Umbral Otsu')

#%%
# HARRIS
# cornerHarris devuelve un mapa de respuesta.
# Los máximos locales corresponden a esquinas.

gray_float = np.float32(gray)
harris = cv2.cornerHarris(gray_float, blockSize=2, ksize=3, k=0.04)
harris = cv2.dilate(harris, None)
plt.figure(14), plt.imshow(harris, cmap='jet'), plt.title('Mapa de respuesta Harris')

harris_vis = img_rgb.copy()
harris_vis[harris > 0.01 * harris.max()] = [0, 0, 255]

plt.figure(9)
plt.imshow(harris_vis, cmap='gray'), plt.title('Harris esquinas')

#%%
# HOUGH PARA LÍNEAS
line_img = img_rgb.copy()

linesP = cv2.HoughLinesP(
    edges_canny,
    rho=1,
    theta=np.pi/180,
    threshold=80,
    minLineLength=40,
    maxLineGap=10
)

if linesP is not None:
    for l in linesP:
        x1, y1, x2, y2 = l[0]
        cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

plt.figure(15) # Cambiado para evitar conflicto con la figura del histograma (Figura 10)
plt.imshow(line_img, cmap='gray'), plt.title('Lineas Hough')

#%%
# HOUGH PARA CÍRCULOS
circles_vis = img_rgb.copy()

circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=40,
    param1=100,
    param2=20,
    minRadius=20,
    maxRadius=90
)

if circles is not None:
    circles = np.round(circles[0, :]).astype(int)
    for (x, y, r) in circles:
        cv2.circle(circles_vis, (x, y), r, (0, 255, 0), 2)
        cv2.circle(circles_vis, (x, y), 2, (0, 0, 255), 3)
        
plt.figure(11)
plt.imshow(circles_vis, cmap='gray'), plt.title('Circulos Hough')

#%%
#####
#EJERCICIO
#####

img_gray = data.coins()

blur = cv2.GaussianBlur(img_gray, (5, 5), 0)


umbral, binaria = cv2.threshold(
    blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binaria, 8)

# Convertimos a RGB para poder dibujar rectángulos en color (Rojo)
resultado = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
conteo = 0

for i in range(1, num_labels):   # 0 = fondo
    x, y, w, h, area = stats[i]

    # Filtrar regiones pequeñas para evitar ruido
    if area > 200:
        conteo += 1
        cv2.rectangle(resultado, (x, y), (x + w, y + h), (255, 0, 0), 2)


print("Número de objetos detectados:", conteo)


plt.figure(12)
plt.imshow(resultado), plt.title('Monedas detectadas')

#%%

img = data.checkerboard()

blur = cv2.GaussianBlur(img, (5, 5), 1.0)

bordes = cv2.Canny(blur, 50, 150)

lineas = cv2.HoughLinesP(
    bordes,
    rho=1,
    theta=np.pi / 180,
    threshold=40,
    minLineLength=50,
    maxLineGap=10
)

# Convertimos a RGB para ver las líneas en color verde
resultado = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
conteo_lineas = 0

if lineas is not None:
    for linea in lineas:
        x1, y1, x2, y2 = linea[0]
        cv2.line(resultado, (x1, y1), (x2, y2), (150, 255, 150), 2)
        conteo_lineas += 1

print("Número de líneas detectadas:", conteo_lineas)
plt.figure(13)
plt.imshow(resultado), plt.title('Líneas detectadas')
plt.show()
