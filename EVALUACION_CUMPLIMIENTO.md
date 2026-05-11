

**Fecha:** Mayo 10, 2026  
**Repositorio:** https://github.com/hssacrament-ui/Proyecto-Analisis-de-Celulas-desde-Imagenes-Microscopio-  


---





**Point Detection** → `point_detection()` con Laplaciano
*Line Detection** → `hough_lines_manual()` 
*Edge Detection** → `edge_detection_sobel()`
*Thresholding** → `otsu_threshold()`
*Region-based Segmentation** → `label_components()`
*Hough Transform** → `hough_circles_manual()`
*Image Preprocessing** → RGB→Gris, Gamma, Filtros


---

 ESTRUCTURA DEL PROYECTO

Proyecto Vision Celulas/
├── cell_segmentation_lib.py       # Librería core (15+ funciones)
├── prueba_unificada.py            # Script unificado de demostración
├── setup.py                       # Configuración de empaquetado
├── requirements.txt               # Dependencias
├── README.md                      # Documentación de usuario
├── reporte_tecnico.md             # Metodología técnica
├── presentacion.md                # Guion de presentación oral
├── Imagen1.png - Imagen10.png     # Dataset de 10 imágenes
└── Masks de prueba 1/             # Máscaras de validación
```

 ALGORITMOS 

1. **Conversión RGB-Gris** - Pesos de luminancia estándar
2. **Corrección Gamma** - Tabla de búsqueda (LUT)
3. **Filtro Gaussiano** - Kernel 2D + convolución
4. **FFT Pasa-Bajos** - Máscara circular en frecuencia
5. **Sobel** - Kernels Kx/Ky con gradientes
6. **Otsu** - Búsqueda exhaustiva de umbral óptimo
7. **Hough Líneas** - Acumulador rho/theta
8. **Hough Círculos** - Búsqueda exhaustiva 3D
9. **Laplaciano** - Detección de puntos

---

##  INSTRUCCIONES DE USO

### Ejecutar Demo:
```bash
cd "Proyecto Vision Celulas"
pip install -r requirements.txt
python prueba_unificada.py
```

### Instalar como Paquete:
```bash
pip install .
```

### Clonar desde GitHub:
```bash
git clone https://github.com/hssacrament-ui/Proyecto-Analisis-de-Celulas-desde-Imagenes-Microscopio-.git
cd "Proyecto-Analisis-de-Celulas-desde-Imagenes-Microscopio-"
pip install -r requirements.txt
python prueba_unificada.py
```


---

**Evaluación completada: 10 de Mayo de 2026**  
**Prepared by:** GitHub Copilot
