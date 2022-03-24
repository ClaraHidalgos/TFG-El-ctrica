import pandas as pd
import matplotlib.pyplot as plt
import pvlib
import numpy as np
import sys
import datetime


"""DESCRIPCIÓN: programa que calcula la irradiancia global que hay en cada sensor  Irradiancia total= Idirecta+ Idifusa + I reflejada"""

def calculo_irr(datos, i, solpos, cs, dni_extra):
    aux = pd.DataFrame(columns=['1'], index=range(5))    
    j = 0
    for y in aux.index: 
        
        if j == 0:
            aoi = pvlib.irradiance.aoi(datos['theta_t_1'][i], datos['theta_z_1'][i],
                                       solpos['apparent_zenith'], solpos['azimuth']) # Angulo solar de incidencia respecto a la superficie
            
            total_irr = pvlib.irradiance.get_total_irradiance(datos['theta_t_1'][i], datos['theta_z_1'][i],
                                                                solpos['apparent_zenith'], solpos['azimuth'],
                                                                cs['dni'], cs['ghi'], cs['dhi'],
                                                                dni_extra=dni_extra,model='haydavies')
            
            datos.at[i, 'I_sup_pv'] = total_irr['poa_global'][0]
            j = j + 1
            
        elif j == 1: 
            aoi = pvlib.irradiance.aoi(datos['theta_t_2'][i], datos['theta_z_2'][i],
                                       solpos['apparent_zenith'], solpos['azimuth']) # Angulo solar de incidencia respecto a la superficie
            
            total_irr = pvlib.irradiance.get_total_irradiance(datos['theta_t_2'][i], datos['theta_z_2'][i],
                                                                solpos['apparent_zenith'], solpos['azimuth'],
                                                                cs['dni'], cs['ghi'], cs['dhi'],
                                                                dni_extra=dni_extra,model='haydavies')
            
            datos.at[i, 'I_front_pv'] = total_irr['poa_global'][0]
            j = j + 1
            
        elif j == 2: 
            aoi = pvlib.irradiance.aoi(datos['theta_t_3'][i], datos['theta_z_3'][i],
                                       solpos['apparent_zenith'], solpos['azimuth']) # Angulo solar de incidencia respecto a la superficie
            
            total_irr = pvlib.irradiance.get_total_irradiance(datos['theta_t_3'][i], datos['theta_z_3'][i],
                                                                solpos['apparent_zenith'], solpos['azimuth'],
                                                                cs['dni'], cs['ghi'], cs['dhi'],
                                                                dni_extra=dni_extra,model='haydavies')
            
            datos.at[i,'I_tras_pv'] = total_irr['poa_global'][0]
            j = j + 1
            
        elif j == 3: 
            aoi = pvlib.irradiance.aoi(datos['theta_t_4'][i], datos['theta_z_4'][i],
                                       solpos['apparent_zenith'], solpos['azimuth']) # Angulo solar de incidencia respecto a la superficie
            
            total_irr = pvlib.irradiance.get_total_irradiance(datos['theta_t_4'][i], datos['theta_z_4'][i],
                                                                solpos['apparent_zenith'], solpos['azimuth'],
                                                                cs['dni'], cs['ghi'], cs['dhi'],
                                                                dni_extra=dni_extra,model='haydavies')
            
            datos.at[i,'I_der_pv'] = total_irr['poa_global'][0]
            j = j + 1
            
        elif j == 4: 
            aoi = pvlib.irradiance.aoi(datos['theta_t_5'][i], datos['theta_z_5'][i],
                                       solpos['apparent_zenith'], solpos['azimuth']) # Angulo solar de incidencia respecto a la superficie
            
            total_irr = pvlib.irradiance.get_total_irradiance(datos['theta_t_5'][i], datos['theta_z_5'][i],
                                                                solpos['apparent_zenith'], solpos['azimuth'],
                                                                cs['dni'], cs['ghi'], cs['dhi'],
                                                                dni_extra=dni_extra,model='haydavies')
            
            datos.at[i,'I_izq_pv'] = total_irr['poa_global'][0]
            j = j + 1
            
            
    return datos
    