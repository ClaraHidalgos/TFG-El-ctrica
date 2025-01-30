import cv2
import numpy as np
import contornos_funcion
import aislar_cielo_funcion

def calcular_svf(mask, n_anillos=20):
    """
    Calcula el Sky View Factor (SVF) basado en una imagen binaria de cielo/no cielo.

    Args:
        mask (numpy.ndarray): Imagen binaria con el cielo en blanco (255) y el resto en negro (0).
        n_anillos (int): Número de anillos concéntricos en los que se dividirá la imagen.

    Returns:
        float: Valor del Sky View Factor (SVF).
    """
    # Dimensiones de la imagen
    h, w = mask.shape
    radio_max = min(h, w) // 2  # Radio máximo, centrado en la imagen

    # Coordenadas del centro de la imagen
    centro_x, centro_y = w // 2, h // 2

    # Inicializar el SVF
    svf = 0

    # Dividir el radio en n_anillos
    radios = np.linspace(0, radio_max, n_anillos + 1)  # Bordes de los anillos

    for i in range(1, len(radios)):
        # Radio interno y externo del anillo
        radio_interno = radios[i - 1]
        radio_externo = radios[i]

        # Crear máscaras para el anillo
        mascara_anillo = np.zeros_like(mask, dtype=np.uint8)
        cv2.circle(mascara_anillo, (centro_x, centro_y), int(radio_externo), 255, thickness=-1)
        cv2.circle(mascara_anillo, (centro_x, centro_y), int(radio_interno), 0, thickness=-1)

        # Contar píxeles en el anillo
        pixeles_anillo = cv2.bitwise_and(mask, mascara_anillo)
        pixeles_cielo = np.sum(pixeles_anillo == 255)
        total_pixeles_anillo = np.sum(mascara_anillo == 255)

        if total_pixeles_anillo > 0:
            # Contribución del anillo al SVF
            peso_anillo = np.sin((np.pi * (2 * i - 1)) / (2 * n_anillos))
            svf += peso_anillo * (pixeles_cielo / total_pixeles_anillo)

    # Escalar el resultado por π / (2 * n)
    svf *= np.pi / (2 * n_anillos)

    return svf



def procesar_imagen(name):
    """
    Función que procesa una imagen para detectar el cielo y calcular el SkyField Value (SFV).
    
    Args:
        nombre_img (str): Nombre de la imagen (sin la extensión).
        formato_img (str): Formato de la imagen, por ejemplo, '.jpg'.
        esquinas (int): Píxeles correspondientes a las esquinas que no deben contarse.
    
    Returns:
        sfv (float): SkyField Value calculado.
    """
    
    """ABRIMOS LA IMAGEN Y DEFINIMOS SU ANCHO Y SU ALTO, w y h respectivamente"""
    img = cv2.imread(name)
    h, w = img.shape[:2]
    new_w = int(1 * w)
    new_h = int(1 * h)
    
    """LLAMAMOS A LA FUNCIÓN aislar_cielo_funcion.azul. -> Lo que hace esta función es aplicar dos máscaras distisntas
    a la imágen. La primera aisla los azules oscuros de la imágen y la otra los azules claritos. Comparando los resultados
    de las dos máscaras se determinará si la imágen es oscura o clara y respecto de eso se le aplicará la máscara corresponiente.
    Devuelve new_mask que es la imágen con resize con la máscara aplicada, en blanco es el cielo y negro no cielo. Mask es
    lo mismo pero en su tamaño original."""
    
    mask = aislar_cielo_funcion.azul(name)


    """LLAMAMOS A LA FUNCIÓN contornos_funcion.contornos-> esta función principlamnete detecta los bordes de la imágen y con
    eso aisla el contorno del cielo, se explica mejor en el propio .py. Nos devuelve new_contornos que corrsponde a  la
    imágen final donde el blanco es el cielo y el resto objetos"""
    
    final = contornos_funcion.contornos(name, mask)

    """Muestro por pantalla la imágen de cielo blanco y demás negro"""
    new_bn = cv2.resize(final, (new_w, new_h))
    # cv2.imshow("imagen_final", new)

    """Muestro por pantalla, la imágen original, y en azul lo que ha salido como cielo """
    h, w = final.shape[:2]

    for i in range(int(h)):
        for j in range(int(w)):
            if final[i][j] == 255:
                img[i][j][0] = 225  # Azul
                img[i][j][1] = 218  # Verde
                img[i][j][2] = 75   # Rojo

    new = cv2.resize(img, (new_w, new_h))
    # cv2.imshow("imagen_final_original", new)

    """ Lee imágenes de una carpeta con el formato 'Cielo_aislado_bn{i}.jpg', cuenta los píxeles blancos
     dentro de un círculo, calcula el porcentaje, y agrega esta información como la columna 'fsv' a un DataFrame"""
    # Obtener las dimensiones de la imagen
    img_fsv = new_bn
    

    """Calculo el sfv como píxeles_correspondientes_al_cielo/píxeles_totales_de_la_imagen"""
    sfv = calcular_svf(img_fsv)*100

    # Mantener las ventanas abiertas hasta que se cierre manualmente

    return new_bn, new, sfv
