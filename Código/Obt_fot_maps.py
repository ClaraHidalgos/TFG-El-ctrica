import google_streetview.api
import cv2
import google_streetview.helpers
import os
from os import remove


def fotos(coordenada_y, coordenada_x, num, nombre_carpeta):
    """
   Utiliza la API de Google Street View para descargar imágenes de 360° alrededor de una ubicación especificada.
   Las imágenes se descargan en diferentes direcciones y se guardan en la carpeta especificada por el usuario

   Args:
       coordenada_y (float): La latitud de la ubicación.
       coordenada_x (float): La longitud de la ubicación.
       num (int): Un número identificativo para nombrar las imágenes.
       nombre_carpeta (str): El nombre de la carpeta donde se guardarán las imágenes descargadas.
   """
   
    
    
    rum=[0,90,180,270,0]
    
    with open('apikey.txt') as f:
        api_key = f.readline()
        f.close
        
    inclinacion = str(0)  # Inclinación lente
    p_h = 640  # Número de pixeles horizontal - máx 640 píxeles
    p_v = 640  # Número de pixeles vertical - máx 640 píxeles
    tamaño = str(p_h)+'x' + str(p_v)  # Tamaño imagen - máx 640x640 píxeles
    # Datos empleados de la ubicacción

    #lat, lon = 40.4168838, -3.6783211  # Latitud y Longitud
    lat, lon = coordenada_y,coordenada_x  # Latitud y Longitud
    localizacion = str(lat) + ',' + str(lon)
    campo_visual_H=str(90)  # Campo de visión horizontal
    
    cont=0;
    
    for i in range(len(rum)):
        
        rumbo = str(rum[i])# Orientación N(0), E(90), S(180), O(270)
        if cont==4:
            inclinacion = str(90)  # Inclinación lente
        
        
        params = [{
          'size': tamaño, # max 640x640 pixels
          'location': localizacion,
          'heading': rumbo,
          'pitch': inclinacion,
          'fov' : campo_visual_H,
          'key': api_key
        }]
    
        # Crea un objeto con el resultado
        results = google_streetview.api.results(params)
    
        # Guarda imagen en la carpeta 'downloads'
        results.download_links('downloads')
        
        carpeta = nombre_carpeta

        # Crear la carpeta si no existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        
        #Cambiamos la foto de posición a una carpeta nueva
        extension = '.jpg'
        carpeta = nombre_carpeta +'/f'
        ruta= carpeta+str(num) + '_' + str(i) + extension
        img=cv2.imread('downloads\gsv_0.jpg')
        #cv2.imshow('foto', img)
        cv2.imwrite( ruta , img)
        remove('downloads\gsv_0.jpg')
        
        cont=cont+1
    
