import os
import cv2
import pandas as pd
import math
import numpy as np

def calcular_porcentaje_pixeles_blancos(carpeta, n, nombre_excel):
    """
    Lee imágenes de una carpeta con el formato 'Cielo_aislado_bn{i}.jpg', cuenta los píxeles blancos
    dentro de un círculo, calcula el porcentaje, y agrega esta información como la columna 'fsv' a un DataFrame.

    Args:
        carpeta (str): Ruta de la carpeta donde se encuentran las imágenes.
        n (int): Número de imágenes a procesar (de 0 a n-1).
        nombre_excel (str): Nombre del archivo Excel a cargar y modificar.

    Returns:
        DataFrame: El DataFrame actualizado con la columna 'fsv'.
    """

    # Leer el archivo Excel en un DataFrame
    puntos2 = pd.read_excel(nombre_excel)

    # Lista para almacenar el porcentaje de píxeles blancos de cada imagen
    fsv = []

    # Recorrer las imágenes
    for i in range(n):
        nombre_imagen = f"Cielo_aislado_bn{i}.jpg"
        ruta_imagen = os.path.join(carpeta, nombre_imagen)

        # Leer la imagen en escala de grises
        img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            print(f"No se pudo leer la imagen: {nombre_imagen}")
            continue

        # Obtener las dimensiones de la imagen
        alto, ancho = img.shape[:2]
        radio = ancho // 2  # Radio del círculo (la imagen es cuadrada)

        # Crear una máscara circular
        centro = (radio, radio)
        mascara_circular = cv2.circle(
            img=np.zeros((alto, ancho), dtype=np.uint8),
            center=centro,
            radius=radio,
            color=255,
            thickness=-1
        )

        # Calcular el número de píxeles dentro del círculo
        pixeles_en_circulo = cv2.countNonZero(mascara_circular)

        # Contar los píxeles blancos dentro del círculo en la imagen
        pixeles_blancos = cv2.countNonZero(cv2.bitwise_and(img, img, mask=mascara_circular))

        # Calcular el porcentaje de píxeles blancos
        porcentaje_blancos = (pixeles_blancos / pixeles_en_circulo) * 100
        fsv.append(porcentaje_blancos)

    # Agregar la nueva columna 'fsv' al DataFrame
    puntos2['fsv % '] = fsv

    # Guardar el DataFrame actualizado en un nuevo archivo Excel
    puntos2.to_excel("Aracena_carretera2/puntos2.xlsx", index=False)
    
    print("El archivo Excel se ha actualizado correctamente.")
    return puntos2

# Ejemplo de uso
carpeta = "Aracena_carretera2"
n = 13  # Número de imágenes a procesar
nombre_excel = "Aracena_carretera2/puntos2.xlsx"
puntos2= calcular_porcentaje_pixeles_blancos(carpeta, n, nombre_excel)
