# Herramienta de Modelado del Recurso Solar y Generación de Energía en Rutas

Este directorio contiene el código necesario para calcular el Sky View Factor (SVF) y modelar la energía generada por un vehículo fotovoltaico en ruta.

## Descripción General

### Funcionalidad
La herramienta desarrollada tiene como objetivo modelar el recurso solar disponible en distintas superficies de un vehículo eléctrico durante rutas, considerando tanto las características del entorno como las propiedades geométricas del vehículo. La herramienta se divide en dos programas principales:

1. **`principal.py`**: Este script genera los puntos intermedios de una ruta, calcula el SVF en cada punto y produce las imágenes correspondientes.
2. **`evaluacion_energia.py`**: Este script evalúa la energía generada en la ruta usando los resultados obtenidos por `principal.py`.

### Datos de Entrada
- **`principal.py`**:
  - Nombre de la carpeta donde se guardarán los resultados.
  - Distancia mínima entre puntos de la ruta.
  - Coordenadas geográficas del origen y destino.

- **`evaluacion_energia.py`**:
  - Resultados generados por `principal.py` (SVF, imágenes y puntos de la ruta).
  - Velocidad media de la ruta.
  - Hora y fecha en la que se desea simular la ruta.

### Datos de Salida
- **`principal.py`**:
  - Excel con los puntos intermedios y su SVF asociado.
  - Imágenes generadas:
    - Vista de ojo de pez.
    - Imágenes individuales que forman la vista de ojo de pez.
    - Imagen binaria con detección de cielo.

- **`evaluacion_energia.py`**:
  - Excels con los valores de irradiancia global y componentes (directa, difusa, reflejada) para cada cara del vehículo.
  - Resultados energéticos totales para cada tramo de la ruta.

---

## Detalles del Funcionamiento

### 1. Generación de Nodos y SVF (`principal.py`)
El usuario introduce un origen y destino con sus coordenadas geográficas, junto con una distancia mínima. La herramienta genera puntos intermedios en la ruta respetando esta distancia mínima. Por cada punto, se obtienen:
- Imágenes 180º del cielo simulando la cámara en el techo del vehículo.
- Detección del porcentaje de cielo visible (SVF).

### 2. Cálculo de la Energía en Ruta (`evaluacion_energia.py`)
Usando los datos generados, se calcula:
- La posición del sol para cada tramo de la ruta.
- La irradiancia total sobre las superficies del vehículo considerando la inclinación y orientación de cada cara.
- La energía generada para cada tramo, asumiendo una eficiencia típica del panel fotovoltaico (18%) y un área específica para cada cara.

---

## Requerimientos
- Python 3.8+
- Librerías: `pvlib`, `numpy`, `pandas`, `opencv`, entre otras (ver archivo `requirements.txt`).
