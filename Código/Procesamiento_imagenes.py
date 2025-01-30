import matplotlib.pyplot as plt
import cv2
from matplotlib.patches import Polygon

from Funciones_cubo_esfera import generar_esfera_3d
from Funciones_cubo_esfera import proyectar_equisolida
from Sky_field_funcion import procesar_imagen

def imagenes(nombre_carpeta, num_puntos):
    """
   Usa un conjunto de imágenes en diferentes orientaciones (frontal, derecha, trasera, izquierda, y superior) desde una 
   carpeta, y las procesa para crear una representación esférica 3D. Después, la función proyecta la esfera en una 
   imagen 2D utilizando una proyección de ojo de pez (equisolida) y genera una representación del cielo aislado en 
   imágenes. También se almacena un vector de resultados procesados de la imagen esférica. Además seprocesa la imágen
   detectando el porcentaje de cielo que hay en esta. Toda la función se apoyaa en otra funciones de otros .py

   Args:
       nombre_carpeta (str): El nombre de la carpeta donde se encuentran las imágenes originales y donde se guardarán las imágenes procesadas.
       num_puntos (int): Número de puntos o imágenes que se van a procesar.
       
       
    Return:
        vector_sfv (list): Una lista que contiene los vectores de valores extraídos después de procesar las imágenes de ojo de pez.

   """
    
    
    
    # CONSTANTES1
    PIXELES_CARA = 100 * 100
    TAMANO = int(PIXELES_CARA ** 0.5)
    sphere_vertices = []
    sphere_col_dec = []
    vector_sfv = []
    
    puntos = num_puntos
    
    for i in range(puntos):
        # Abrir las imágenes
        ruta = nombre_carpeta +"/f" + str(i) + "_" + str(0)+'.jpg'
        imagen_front = cv2.imread(ruta)
        imagen_front_re = cv2.resize(imagen_front, (TAMANO, TAMANO))
        
        ruta = nombre_carpeta +"/f" + str(i) + "_" + str(1)+'.jpg'
        imagen_rface = cv2.imread(ruta)
        imagen_rface_re = cv2.resize(imagen_rface, (TAMANO, TAMANO))
        
        ruta = nombre_carpeta +"/f"+ str(i) + "_" + str(2)+'.jpg'
        imagen_back = cv2.imread(ruta)
        imagen_back_re = cv2.resize(imagen_back, (TAMANO, TAMANO))
        
        ruta = nombre_carpeta +"/f" + str(i) + "_" + str(3)+'.jpg'
        imagen_lface = cv2.imread(ruta)
        imagen_lface_re = cv2.resize(imagen_lface, (TAMANO, TAMANO)) 
        
        ruta = nombre_carpeta +"/f" + str(i) + "_" + str(4)+'.jpg'
        imagen_top = cv2.imread(ruta)
        imagen_top_re = cv2.resize(imagen_top, (TAMANO, TAMANO))
        
        
        # Generamos la esfera-> esta función devuelve los puntos de la esfera
        
        # Crear la figura y el eje 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        sphere_vertices, sphere_col_dec, ax = generar_esfera_3d(imagen_front_re, imagen_top_re, imagen_back_re, imagen_rface_re, imagen_lface_re, TAMANO, ax)
        
        # Generamos la imagen en 2D proyectando la esfera 
        # Crear una figura 2D para proyectar los cuadrados
        fig_2d, ax_2d = plt.subplots()
    
        # Definir el tamaño del gráfico 2D
        ax_2d.set_xlim(-1, 1)  # El rango en el eje X para un radio de 1
        ax_2d.set_ylim(-1, 1)  # El rango en el eje Y para un radio de 1
        for vertices, color in zip(sphere_vertices, sphere_col_dec):
            # Proyectar el cuadrado usando la proyección perspectiva
            projected_vertices =  proyectar_equisolida(vertices)
            
            # Crear un polígono en el plano XY con las coordenadas proyectadas
            polygon = Polygon(projected_vertices, color=color, edgecolor='none')
            
            # Añadir el polígono a la imagen 2D
            ax_2d.add_patch(polygon)
            
        # Mostrar la proyección 2D final
        ax_2d.set_aspect('equal')
        # Ocultar los ejes
        ax_2d.axis('off') # Esto elimina los bordes y los ejes

        # Guardar la figura sin márgenes y sin los ejes
        fig_2d.savefig( nombre_carpeta +"/" + 'fish_eye'+str(i)+'.jpg' , bbox_inches='tight', pad_inches=0)
        
        new_1, new, sfv = procesar_imagen( nombre_carpeta +"/" + 'fish_eye'+str(i)+'.jpg')
        
        vector_sfv.append(sfv)
        cv2.imshow('imagen_m2'+str(i), new_1)  
        #cv2.imshow('imagen_m1'+str(i), new)
        cv2.imwrite(nombre_carpeta +"/" + 'Cielo_aislado_bn'+str(i)+'.jpg' , new_1)
        cv2.imwrite(nombre_carpeta +"/" + 'Cielo_aislado'+str(i)+'.jpg' , new)
    
        # Show plot
        #plt.show(block=False)  
        
    return vector_sfv


    



