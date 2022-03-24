import pandas as pd
import matplotlib.pyplot as plt
import pvlib
import ang_az_ti 
import cambio_formato_fecha
import obtencion_tempair_windspeed
import numpy as np
import sys
import datetime
import calculo_irr_global


"""-------------------VARIABLES QUE *NO* SE DEBEN MODIFICAR---------------------------"""
i = 0


"""ABRIMOS NUESTROS ARCHIVOS DE DATOS: el .txt de la estación meteo y el excel de ThinkSpeak"""
file_TS1_1 = pd.read_excel('datos_22_02_22.xlsx')
file_TS2 = pd.read_excel('feeds.xlsx')
file_meteo_junto = pd.read_csv('meteo2022_02_10.txt')
name = "yyyy/mm/dd hh:mm\tTemp. Ai 1\tBn\tGh\tDh\tCelula Top\tCelula Mid\tCelula Bot\tTop - Cal \tMid - Cal \tBot - Cal \tPresion\tV.Vien.1\tD.Vien.1\tElev.Sol\tOrient.Sol\tTemp. Ai 2\tHum. Rel\tBn_2\tG(41)\tGn\tPirgeo\tTemp_Pirgeo\tAuxil.01\tV.Vien.2\tD.Vien.2\tLluvia\tLimpieza\tElev.Sol_2\tOrient.Sol_2"
file_meteo = file_meteo_junto[name].str.split(expand=True) # hemos dividido los datos, ya que estaban todos en la misma columna

tamaño_chanel_1 = np.shape(file_TS1_1)
tamaño_chanel_2 = np.shape(file_TS2)
if tamaño_chanel_1[0] != tamaño_chanel_2[0]:
    print("Los archivos procedentes de ThingSpeak no tienen el mismo número de columnas, por favor reviseló\n")
    sys.exit()


"""ZONA HORARIA, MÓDULO E INVERSOR"""
zona_horaria = 'Etc/GMT-1' # OJOOOOO LA ZONA HORARIA SE PONE AL REVÉS
sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
sapm_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')
module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
inverter = sapm_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']


"""DATOS QUE PROVIENEN DE THING_SPEAK PARA EL CÁLCULO DE LA IRR: hora (1columna del 1 canal) y 
                            ángulo(7 columna del 2 canal) """
# Hay que cambiar el formato de la hora de: 2022-02-22T15:27:45+01:00 a	2022-02-22 15:27:45-01:00
file_TS1 = cambio_formato_fecha.cambio_formato_fecha(file_TS1_1)
times = file_TS1['Fecha']
angulos = ang_az_ti.angulos_data_frame(file_TS2['field7'])


"""DATOS QUE PROVIENEN DE METEO (datos de la estación meteorológica) PARA EL CÁLCULO DE LA IRR: velocidad 
del viento (columna 20 CREOOOO) y temperatura del aire (columna 3 CREOOOO) """

temp_speed = obtencion_tempair_windspeed.temp_speed(file_TS1, file_meteo)
temp_air = temp_speed['TEMP_AIR']
wind_speed = temp_speed['WIND_SPEED']



"""CREO UN DATAFRAME CONJUNTO PARA TODOS LOS DATOS QUE SE VAN A USAR"""

datos = pd.DataFrame(columns= ['HORA_DIA','TEMP_AIR', 'WIND_SPEED', 'LATITUD', 'LONGITUD', 'ALTITUD', 
                               'theta_z_1', 'theta_t_1', 'I_sup_pv', 'I_sup_sens', 'theta_z_2', 'theta_t_2', 
                               'I_front_pv', 'I_front_sens','theta_z_3', 'theta_t_3',  'I_tras_pv', 
                               'I_tras_sens', 'theta_z_4', 'theta_t_4',   'I_der_pv', 'I_der_sens',
                                'theta_z_5', 'theta_t_5', 'I_izq_pv', 'I_izq_sens'], index = range(tamaño_chanel_1[0]))



datos['HORA_DIA'] = times # a la hora de usar pvlib no se va a poder usar datos['HORA_DIA'] ya que es una serie y nosotros necesitamos DatetimeIndex
datos['TEMP_AIR'] = temp_air
datos['WIND_SPEED'] = wind_speed
datos['LATITUD'] = file_TS2['field1']
datos['LONGITUD'] = file_TS2['field2']
datos['ALTITUD'] = file_TS2['field3']

datos['theta_z_1'] = angulos['theta_z_1']
datos['theta_t_1'] = angulos['theta_t_1']
datos['theta_z_2'] = angulos['theta_z_2']
datos['theta_t_2'] = angulos['theta_t_2']
datos['theta_z_3'] = angulos['theta_z_3']
datos['theta_t_3'] = angulos['theta_t_3']
datos['theta_z_4'] = angulos['theta_z_4']
datos['theta_t_4'] = angulos['theta_t_4']
datos['theta_z_5'] = angulos['theta_z_5']
datos['theta_t_5'] = angulos['theta_t_5']

datos['I_sup_sens'] = file_TS1['I_sup']
datos['I_front_sens'] = file_TS1['I_front']
datos['I_tras_sens']= file_TS1['I_tras']
datos['I_der_sens']= file_TS1['I_der']
datos['I_izq_sens'] = file_TS1['I_izq']

"""Hay que cambiar el formto de times para que lo puda usar pvlib"""
times=pd.to_datetime(times,utc=False) # hay que pasar las horas a formato de pandas
times = cambio_formato_fecha.cambio_datatime(times, zona_horaria)

"""CÁLCULO LA IRRADIANCIA CON PVLIB"""
for x in datos.index:

    """--ÁNGULOS QUE DEFINEN LA POSICIÓN DEL SOL Y IRRADIANCIA NORMAL DIRECTA--"""
    timess = cambio_formato_fecha.time_to_tl(times[i], zona_horaria)
    solpos = pvlib.solarposition.get_solarposition(timess , datos['LATITUD'][i], datos['LONGITUD'][i])
    dni_extra = pvlib.irradiance.get_extra_radiation(times[i])
    
    """---------------------AIRMASS ABS, DHI, DNI Y GHI-------------------------"""
    airmass = pvlib.atmosphere.get_relative_airmass(solpos['apparent_zenith']) # devuelve el airmass relativo
    pressure = pvlib.atmosphere.alt2pres(datos['ALTITUD'][i]) # presión a esa altitud
    am_abs = pvlib.atmosphere.get_absolute_airmass(airmass, pressure) #Deveuelve el airmass a esa altura especifica
    tl = pvlib.clearsky.lookup_linke_turbidity(timess, datos['LATITUD'][i], datos['LONGITUD'][i]) # Factor LINKE TURBIDITY, describe el esp. óptico de la atm. por la abs. por el vapor de 
    # agua como a la abs. y disp. por las partículas de aerosol. Resume la turbidez de la atmósfera y, por tanto, la atenuación de la radiación solar directa.
    cs = pvlib.clearsky.ineichen(solpos['apparent_zenith'], am_abs, tl, dni_extra=dni_extra, altitude=datos['ALTITUD'][i]) # devuelve DHI (irr. horizontal), DNI Y GHI (global horizontal)
    

    """----------------ANGULO SOLAR DE INCIDENCIA E IRRADIANCIA TOTAL-------------"""
    datos = calculo_irr_global.calculo_irr(datos, i, solpos, cs, dni_extra)
 
    i = i+1
    
    
"""LO EXPORTAMOS A EXCEL"""

file_name = 'Resultados' + file_TS1['Fecha'][0][0:10] +'.xlsx'
datos.to_excel(file_name)
