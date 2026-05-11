# Reporte Técnico: Segmentación de Células

## Metodología
El sistema utiliza un pipeline de procesamiento de imágenes para aislar núcleos celulares:

1.  **Mejora de Imagen**: Se aplica Corrección Gamma para resaltar objetos tenues y Filtrado Gaussiano para reducir el ruido.
2.  **Dominio de la Frecuencia**: Se implementó un Filtro Pasa Bajos mediante FFT para suavizar texturas de fondo complejas.
3.  **Segmentación Adaptativa**: Se utiliza el algoritmo de Otsu (implementado manualmente) para encontrar el umbral óptimo de binarización sin intervención del usuario.
4.  **Análisis Morfológico**: Mediante el etiquetado de componentes conectados, se discriminan objetos por área para eliminar falsos positivos (ruido o detritos).

## Resultados
El sistema fue validado con un dataset de 10 imágenes de microscopía con diferentes niveles de exposición y densidad celular, logrando una alta correlación con el conteo manual. 8 de 10 imagenes contaron bien

## Conclusiones
La implementación de algoritmos usando NumPy permite un control preciso sobre los parámetros de segmentación, resultando en una herramienta sencilla para uso escolar.
