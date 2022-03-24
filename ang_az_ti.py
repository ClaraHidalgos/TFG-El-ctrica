import pandas as pd
import matplotlib.pyplot as plt
import pvlib
import numpy as np

"""PROGRAMA QUE DEVUELVE LOS ÁNGULOS AZIMUTH Y TILT DE CADA CARA DEL COCHE DADO EL ÁNGULO DE AZIMUTH DE LA CARA FRONTAL """

def angulos(module, inverter, a):

# CARA SUPERIOR
    theta_z_1 = 0
    theta_t_1 = 0
    #return(theta_z_1, theta_t_1)

# CARA FRONTAL
    theta_z_2 = a
    theta_t_2 = 15
    #return(theta_z_2, theta_t_2)

# CARA TRASERA
    if a < 180:
        theta_z_3 = a + 180 
    else:
        theta_z_3 = a - 180

    theta_t_3 = 45
    #return(theta_z_3, theta_t_3)

# CARA LATERAL DERECHA
    if a < 270:
        theta_z_4 = a + 90 
    else:
        theta_z_4 = a - 270
    print(theta_z_4)
    theta_t_4 = 90
    
    #return(theta_z_4, theta_t_4)

# CARA LATERAL IZQUIERDA
    if a < 90 :
        theta_z_5 = a + 270 
    else:
        theta_z_5 = a - 90

    theta_t_5 = 90
    system = [{'module': module, 'inverter': inverter,'surface_azimuth': theta_z_1, 'surface_tilt': theta_t_1}, 
              {'module': module, 'inverter': inverter,'surface_azimuth': theta_z_2, 'surface_tilt': theta_t_2}, 
              {'module': module, 'inverter': inverter,'surface_azimuth': theta_z_3, 'surface_tilt': theta_t_3},
              {'module': module, 'inverter': inverter,'surface_azimuth': theta_z_4, 'surface_tilt': theta_t_4},
              {'module': module, 'inverter': inverter,'surface_azimuth': theta_z_5, 'surface_tilt': theta_t_5}] 
    
    return system


"""-------------------------------------------------------------------------------------------------------------------------------------------------------------------"""


""" Hace lo mismo que la función de arriba pero en vez de con un solo ángulo con varios ángulos y o alamacena en un dataframe"""
def angulos_data_frame(angulo):
    
    i = 0
    
    num_datos = np.shape(angulo) # nos devuelve el tamaño de angulo para poder saber cuantas medidas de ángulos hay y lueg crear df con tel tamaño correcto
    
    df = pd.DataFrame(columns=['theta_z_1', 'theta_t_1', 'theta_z_2', 'theta_t_2','theta_z_3', 'theta_t_3','theta_z_4', 'theta_t_4', 'theta_z_5', 'theta_t_5'],
                      index=range(num_datos[0])) # dataframe que va a recoger el ángulo amiuth y tilt de cada cara del sensor
    
    
    for x in angulo:
        # CARA SUPERIOR
            df['theta_z_1'][i] = 0
            df['theta_t_1'][i] = 0
    
        # CARA FRONTAL
            df['theta_z_2'][i] = angulo[i]
            df['theta_t_2'][i] = 15
    
        # CARA TRASERA
            if angulo[i] < 180:
                df['theta_z_3'][i] = angulo[i] + 180 
            else:
                df['theta_z_3'][i] = angulo[i] - 180
    
            df['theta_t_3'][i] = 45
    
        # CARA LATERAL DERECHA
            if angulo[i] < 270:
                df['theta_z_4'][i]= angulo[i] + 90 
            else:
                df['theta_z_4'][i] = angulo[i] - 270
                
            df['theta_t_4'][i] = 90

        # CARA LATERAL IZQUIERDA
            if angulo[i] < 90 :
                df['theta_z_5'][i] = angulo[i] + 270 
            else:
                df['theta_z_5'][i] = angulo[i] - 90
    
            df['theta_t_5'][i] = 90
            
        # ACTUALIZO EL CONTADOR    
            i = i + 1
        
    return df 