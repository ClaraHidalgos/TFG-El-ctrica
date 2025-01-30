import cv2


def contornos(name, mask):

    """
     Función que procesa una imagen especificada para detectar contornos y luego usa esta información para generar una 
     máscara. La máscara se modifica para resaltar áreas específicas alrededor del centro de la imagen,
     pintando estas regiones basándose en la detección de contornos. La función sigue varios pasos, como convertir 
     la imagen a escala de grises, aplicar un filtro para suavizarla, detectar bordes, y recorrer los píxeles para
     identificar áreas dentro de los bordes y marcar estas áreas en la máscara.
     
     Args:
         name (str): El nombre o la ruta del archivo de la imagen que se va a procesar. 
         mask (numpy.ndarray): Una matriz de imagen (máscara) que se usa para pintar las áreas que cumplen con ciertas condiciones basadas en la detección de contornos. 
     
     Returns:
         mask (numpy.ndarray): La máscara modificada, que es una matriz de imagen donde se han pintado de blanco (255)
         las áreas detectadas según los contornos y condiciones aplicadas en la función.
    """ 
     
    """ PARÁMETROS QUE NO SE PUEDEN MODIFICAR"""
    num = 0
    
    """LEEMOS LA FOTO"""
    img = cv2.imread(name)
    #img = cv2.resize(img, (600, 600))
    img_1 = img
    
    
    h,  w = img.shape[:2]
    new_w= int(1*w)
    new_h = int(1*h)
    new = cv2.resize(img, (new_w, new_h))
    
    #cv2.imshow("imagen_color", new)
    
    
    """1. Vamos a detectar los bordes en la imágen para ello:"""
    """    1.1. Pasamos la imágen a escala de grises:"""
    img_grey = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
    #img_grey = cv2.resize(img_grey, (600, 600))
    # Muestro la imágen
    new = cv2.resize(img_grey, (new_w, new_h))
    #cv2.imshow("imagen_grises", new)
    
    
    """    1.2. Filtrado de ruido de la imagen, se pueden usar dos, Laplaciano y Gauss. Después de muchas
    pruebas se ha visto que en de Laplace funciona mejor para nosotros."""
    
    img_lap = cv2.GaussianBlur(img_grey, (5,5), 0)
    
    #img_lap = cv2.Laplacian(img_grey, cv2.CV_8U)
    # Muestro la imágen
    new = cv2.resize(img_lap, ( new_w, new_h ) )
    #cv2.imshow("imagen_lap", new)
    
    
    
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    
    """    1.2. Detector de bordes Canny"""
    img_canny_lap = cv2.Canny(img_lap, 35, 100)
    new = cv2.resize(img_canny_lap, ( new_w, new_h ) )
    #cv2.imshow("imagen_canny_gauss", new)
    
    
    
    """    1.3. Detector de contornos (líneas continuas)"""
    
    (contornos_can_lap, jerarquia) = cv2.findContours(img_canny_lap.copy(), cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE )
    
    """    1.4. Pinto los contornos e distintas imágenes"""
    """     1.4.1. En la imágen original en negro"""
    cv2.drawContours(img_1,contornos_can_lap,-1,(0,0,0), 3)
    new = cv2.resize(img_1, ( new_w, new_h ) )
    #cv2.imshow("contornos_cann_lap", new)
    
    
    
    
    """     1.4.1. En la imágen hsv en blanco"""
    cv2.drawContours(img_hsv,contornos_can_lap,-1,(255,255,255), 3)
    new = cv2.resize(img_hsv, ( new_w, new_h ) )
    #cv2.imshow("contornos_hsv", new)
    
    
    """ 2. Vamos a ir desde el centro de la foto por cuadrantes hasta que lleguemos a un borde, y esa zona la pinto de
    azul, primero se irá recorriendo 'x' y luego 'y' y después se unirá lo detectado"""
    
    """    2.1. Mantenemos cte la x img_hsv[x] [y] en el segundo bucle"""
    
    
    for i in range(int(h/2)):
        if (img_hsv[int(h/2)+i][int(w/2)][0] ==255 and img_hsv[int(h/2)+i][int(w/2)][1]==255 and img_hsv[int(h/2)+i][int(w/2)][2]==255):
            break
        for j in range(int(w/2)):
            if (img_hsv[int(h/2)+i][int(w/2)+j][0] ==255 and img_hsv[int(h/2)+i][int(w/2)+j][1]==255 and img_hsv[int(h/2)+i][int(w/2)+j][2]==255):
                break
            else:
                num = num + 1
                mask[int(h/2)+i][int(w/2)+j] = 255
                
    for i in range(int(h/2)):
        if (img_hsv[int(h/2)-i][int(w/2)][0] ==255 and img_hsv[int(h/2)-i][int(w/2)][1]==255 and img_hsv[int(h/2)-i][int(w/2)][2]==255):
            break
        for j in range(int(w/2)):
            if (img_hsv[int(h/2)-i][int(w/2)+j][0]==255 and img_hsv[int(h/2)-i][int(w/2)+j][1]==255 and img_hsv[int(h/2)-i][int(w/2)+j][2]==255):
                break
            else:
                num = num + 1
                mask[int(h/2)-i][int(w/2)+j] = 255
                
    for i in range(int(h/2)):
        if (img_hsv[int(h/2)+i][int(w/2)][0] ==255 and img_hsv[int(h/2)+i][int(w/2)][1]==255 and img_hsv[int(h/2)+i][int(w/2)][2]==255):
            break
        for j in range(int(w/2)):
            if (img_hsv[int(h/2)+i][int(w/2)-j][0]==255 and img_hsv[int(h/2)+i][int(w/2)-j][1]==255 and img_hsv[int(h/2)+i][int(w/2)-j][2]==255):
                break
            else:
                num = num + 1
                mask[int(h/2)+i][int(w/2)-j] = 255
                
    for i in range(int(h/2)):
        if (img_hsv[int(h/2)-i][int(w/2)][0] ==255 and img_hsv[int(h/2)-i][int(w/2)][1]==255 and img_hsv[int(h/2)-i][int(w/2)][2]==255):
            break
        for j in range(int(w/2)):
            if (img_hsv[int(h/2)-i][int(w/2)-j][0]==255 and img_hsv[int(h/2)-i][int(w/2)-j][1]==255 and img_hsv[int(h/2)-i][int(w/2)-j][2]==255):
                break
            else:
                num = num + 1
                mask[int(h/2)-i][int(w/2)-j] = 255
                
    
              
    """    2.2. Mantenemos cte la y img_hsv[x] [y] en el segundo bucle"""
    
    for j in range(int(w/2)):
        if (img_hsv[int(h/2)][int(w/2)+j][0] ==255 and img_hsv[int(h/2)][int(w/2)+j][1]==255 and img_hsv[int(h/2)][int(w/2)+j][2]==255):
            break
        for i in range(int(h/2)):
            if (img_hsv[int(h/2)+i][int(w/2)+j][0] ==255 and img_hsv[int(h/2)+i][int(w/2)+j][1]==255 and img_hsv[int(h/2)+i][int(w/2)+j][2]==255):
                break
            else:
                num = num + 1
                mask[int(h/2)+i][int(w/2)+j] = 255
                
    
    for j in range(int(w/2)):
        if (img_hsv[int(h/2)][int(w/2)+j][0] ==255 and img_hsv[int(h/2)][int(w/2)+j][1]==255 and img_hsv[int(h/2)][int(w/2)+j][2]==255):
            break
        for i in range(int(h/2)):
            if (img_hsv[int(h/2)-i][int(w/2)+j][0]==255 and img_hsv[int(h/2)-i][int(w/2)+j][1]==255 and img_hsv[int(h/2)-i][int(w/2)+j][2]==255):
                break
            else:
                num = num + 1
                mask[int(w/2)-i][int(w/2)+j] = 255
                
    
    for j in range(int(w/2)):
        if (img_hsv[int(h/2)][int(w/2)-j][0] ==255 and img_hsv[int(h/2)][int(w/2)-j][1]==255 and img_hsv[int(h/2)][int(w/2)-j][2]==255):
            break
        for i in range(int(h/2)):
            if (img_hsv[int(h/2)+i][int(w/2)-j][0]==255 and img_hsv[int(h/2)+i][int(w/2)-j][1]==255 and img_hsv[int(h/2)+i][int(w/2)-j][2]==255):
                break
            else:
                num = num + 1
                mask[int(h/2)+i][int(w/2)-j] = 255
                
    
    for j in range(int(w/2)):
        if (img_hsv[int(h/2)][int(w/2)-j][0] ==255 and img_hsv[int(h/2)][int(w/2)-j][1]==255 and img_hsv[int(h/2)][int(w/2)-j][2]==255):
            break
        for i in range(int(h/2)):
            if (img_hsv[int(h/2)-i][int(w/2)-j][0]==255 and img_hsv[int(h/2)-i][int(w/2)-j][1]==255 and img_hsv[int(h/2)-i][int(w/2)-j][2]==255):
                break
            else:
                num = num + 1
                mask[int(h/2)-i][int(h/2
                                     )-j] = 255
             
    
    """    2.3. Pintamos lo obtenido"""        
    new = cv2.resize(img_hsv, ( new_w, new_h ) )
    #cv2.imshow("contornos_hsv_azul", new)
    
    return  mask
    