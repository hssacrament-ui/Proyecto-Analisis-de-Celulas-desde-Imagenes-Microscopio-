from setuptools import setup, find_packages # Importa las utilidades estándar para empaquetar proyectos Python

setup( # Configura los metadatos y requerimientos de la librería
    name="cell_segmentation_lib", # Define el nombre del paquete para la instalación
    version="0.1", # Establece la versión inicial del desarrollo
    packages=find_packages(), # Detecta automáticamente los directorios que contienen código (__init__.py)
    install_requires=[ # Lista las dependencias externas que se instalarán automáticamente
        "numpy", # Necesaria para cálculos matemáticos
        "scipy", # Necesaria para convoluciones y etiquetado
        "matplotlib", # Necesaria para las gráficas de resultados
        "opencv-python", # Necesaria para la manipulación básica de imágenes
    ],
) # Cierra la configuración de setup