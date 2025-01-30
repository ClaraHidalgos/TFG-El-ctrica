import cv2
import numpy as np


def azul(name):
    
    """
     Detecta las áreas de color azul mediante filtros de color en el espacio de color HSV (Hue, Saturation, Value). Se aplican 
     dos máscaras diferentes que delimitan distintos rangos de azul, y se elige la máscara que cubra una mayor cantidad 
     de píxeles de color azul. Finalmente, la función devuelve la imagen redimensionada con las áreas azules resaltadas y 
     la máscara seleccionada
     
     Args:
         name (str): El nombre o la ruta del archivo de la imagen que se va a procesar. 
         
     Returns:
         new (numpy.ndarray):  imagen que muestra las áreas azules detectadas por la máscara seleccionada. 
         mask (numpy.ndarray): La máscara binaria que resalta las áreas de la imagen original que están dentro del 
         rango de color azul definido. Las áreas detectadas son de color blanco (255), y el resto es negro (0).
    """ 

    """PARAMETROS QUE NO SE PUEDEN MODIFICAR"""
    negro = 0
    
    """LEEMOS LA FOTO"""
    img = cv2.imread(name)
    img_1 = img
    img_2 = img
    
    h,  w = img.shape[:2]
    new_w= int(w*1)
    new_h = int(h*1)
    new = cv2.resize(img, (new_w, new_h))
    #cv2.imshow("imagen_color", new)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    """HACEMOS UN FILTRO DE AZUL EN LA FOTO"""
    """    Primero definimos los límtes de nuestra máscara"""
    # Máscara 1
    
    
    lower_blue1 = np.array([75, 60, 190])
    upper_blue1 = np.array([135, 255, 255])
    mask1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
    
    
    lower_blue2 = np.array([60, 10, 50])
    upper_blue2 = np.array([135, 255, 190])
    
    mask2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
    
    
    blanco1 = np.sum(mask1 == 255)
    blanco2 = np.sum(mask2 == 255)
    
    if blanco1>=blanco2:
        new = cv2.resize(mask1, (new_w, new_h))
        mask = mask1
        blanco = blanco1
        #cv2.imshow("imagen_m1", new) 
        #cv2.imwrite('imagen_m1.png', mask1)
    elif blanco1<blanco2:        
        new = cv2.resize(mask2, (new_w, new_h))
        mask = mask2
        blanco = blanco2
        #cv2.imshow("imagen_m2", new)            
        #cv2.imwrite('imagen_m1.png', mask2)   
        
    #cv2.imshow("imagen_color1", cv2.resize(mask, (new_w, new_h)) )

    return  mask




