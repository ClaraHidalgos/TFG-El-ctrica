import pandas as pd
import matplotlib.pyplot as plt
import pvlib

# PROGRAMA QUE DEVUELVE LOS ÁNGULOS AZIMUTH Y TILT DE CADA CARA DEL COCHE DADO EL ÁNGULO DE AZIMUTH DE LA CARA FRONTAL #

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