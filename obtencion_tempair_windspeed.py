import pandas as pd
import matplotlib.pyplot as plt
import pvlib
import numpy as np
import sys

"""Progrma que coge los datos de la temperatura del aire y la velocidad de la estación meteorológica y lo ponen en
el formato que necesitamos. La estacion nos da los datos cada minuto, en cambio, nosotros los cogemos de forma variable,
puede ser cada 20s o cada hora pero hay que unificar el formato. Habrá una función para la temperatura de aire y
otra para la velocidad del viento """

def temp_speed(file_TS1, file_meteo):
    i = 0 # para recorrer el fichero TS1
    w = 0 # PARA COMPROBAR SI NO HAN COINCIDIDO NINGUNA HORA

    
    tamaño = np.shape(file_TS1)
    df = pd.DataFrame(columns = ['TEMP_AIR', 'WIND_SPEED'],index=range(tamaño[0]))


    for a in file_TS1.index:
        j = 0
        for b in file_meteo.index:
            """OJO-> no se comprara la fecha aún porque los archivos que se tienen son de distintos días"""
            if (file_TS1['Fecha'][i][11:13] == file_meteo[1][j][0:2]) and (file_TS1['Fecha'][i][14:16] == file_meteo[1][j][3:5]):
                df['TEMP_AIR'][i] =  file_meteo[2][j]
                df['WIND_SPEED'][i] =  file_meteo[21][j]
                w = w + 1
    
            j = j + 1
        i = i + 1        
    
    if w == 0:
        print("CUIDADO: revise sus archivos porque no coincide ninguna hora entre el canal 1 de ThingSpeak y los datos de la estación meteorológica ")
        sys.exit()
    
    return df 
    # (file_TS1['Fecha'][i][0:4] == file_meteo[0][j][0:4]) and (file_TS1['Fecha'][i][5:7] == file_meteo[0][j][5:7]) and (file_TS1['Fecha'][i][8:10] == file_meteo[0][j][5:7]) and (file_TS1['Fecha'][i][11:13] == file_meteo[1][j][0:2]) and (file_TS1['Fecha'][i][14:16] == file_meteo[1][j][3:5])