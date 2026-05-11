# CellSegmentationLib: Conteo Automático de Células

Librería de visión artificial para la segmentación y conteo de células en imágenes de microscopía, desarrollada con implementaciones manuales de algoritmos fundamentales.

##  Inicio Rápido (Descargar y Usar)

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

1. **Clonar o descargar** este repositorio.
2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Ejecutar la demostración**:
   ```bash
   python prueba_unificada.py
   ```

## 🛠️ Contenido del Proyecto
- `cell_segmentation_lib.py`: Librería core con algoritmos manuales (Gamma, FFT, Sobel, Otsu).
- `prueba_unificada.py`: Script que procesa el dataset de 10 imágenes y muestra resultados visuales.
- `reporte_tecnico.md`: Documentación detallada de la metodología y algoritmos.
- `presentacion.md`: Guion estructurado para la exposición del proyecto.

## Características Técnicas
- Preprocesamiento (Conversión a Gris, Gamma).
- Filtrado Espacial y en Frecuencia (FFT).
- Segmentación (Otsu y Etiquetado de Componentes).
- Detección de Bordes (Sobel) y Transformadas de Hough.

## Instalación
Si deseas usar la librería en otros proyectos:
```bash
pip install .
```

## Uso

Ejecuta el script unificado para procesar todas las imágenes automáticamente:
```bash
python prueba_unificada.py
```

Desarrollado con NumPy, SciPy y OpenCV para apoyo general.