import pandas as pd
import matplotlib.pyplot as plt
import pvlib
import ang_az_ti 

#--ESTE PROGRAMA COMPARA LOS DATOS OBTENIDOS DE UN EXCEL CON LO QUE SIMULA PVLIB Y LUEGO LO EXPORTA A EXCEL--3#
"""-------------------VARIABLES QUE *NO* SE DEBEN MODIFICAR---------------------------"""
i = 0
j = 0
uno = pd.DataFrame()
"""-------------------------*IMPORTAR LOS DATOS DE EXCEL*-------------------------"""
file = pd.read_excel('datos4_22_02_22.xlsx')


"""----*FIJAMOS EL RANGO DE TIEMPO Y LA FRECUENCIA CON LA QUE SE QUIEREN LOS DATOS-*----"""
naive_times =  pd.date_range(start='2022-02-22 17:22:53', end='2022-02-22 17:28:34', freq='20s')


"""Coordenadas-> igual para las 5 placas"""
# Coger del fichero o manualmente del sensor Latitud = Latitud geográfica; Longitud = Longitud geográfica ; altitud = altitud geográfica
coordinates = [40.453, -3.727, 'Madrid', 682, 'Etc/GMT-1'] # Latitud, Longitud, Lugar, altitud y zona horaria        


"""--------DATOS A *CAMBIAR POR EL USUARIO* DE: modelado, módulo, inversor------------"""
sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
sapm_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')
module = sandia_modules['Canadian_Solar_CS5P_220M___2009_'] # No sé cual es la nuestra
inverter = sapm_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']
temperature_model_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

# CONSTANTES DEL AIRE (habrá que medirlo en el momento):
TEMP_AIR = 20
WIND_SPEED = 0
AZ_F = 0 # Valor del ángulo azimuth de la cara frontal

"""---*CRECIÓN DEL SISTEMA CON ANG_AZ_TI: una lista de 5 diccionarios, uno por cada sensor 
            y contiene tipo de modulo, inversor, azimuth e inclinación *---"""
system = ang_az_ti.angulos(module, inverter,87)

energies = {} 

"""---CREACIÓN DEL DATAFRAME CONJUNTO: serán 10 columnas que corresponden a irradiancias 
                medidas e irradiancias sacadas con la simulación---"""
union_datos = pd.DataFrame(columns = ['I_sup_pv', 'I_sup_sens', 'I_front_pv', 'I_front_sens', 'I_tras_pv', 'I_tras_sens', 'I_der_pv', 'I_der_sens', 'I_izq_pv', 'I_izq_sens', ])
union_datos['I_sup_sens'] = file['I_sup']
union_datos['I_front_sens'] = file['I_front']
union_datos['I_tras_sens']= file['I_tras']
union_datos['I_der_sens']= file['I_der']
union_datos['I_izq_sens'] = file['I_izq']



a = file['I_sup']

""" -------CÁLCULO DE IRRADIANCIA EN CADA CARA Y AÑADIRLO A UNION_DATOS------"""
for s in system:
    latitude, longitude, name, altitude, timezone = coordinates
    times = naive_times.tz_localize(timezone) # zona horaria 
    
    
    """--ÁNGULOS QUE DEFINEN LA POSICIÓN DEL SOL Y IRRADIANCIA NORMAL DIRECTA--"""
    solpos = pvlib.solarposition.get_solarposition(times, latitude, longitude) # times, latitud, longitud
    dni_extra = pvlib.irradiance.get_extra_radiation(times)
    
    """---------------------AIRMASS ABS, DHI, DNI Y GHI-------------------------"""
    airmass = pvlib.atmosphere.get_relative_airmass(solpos['apparent_zenith']) # devuelve el airmass relativo
    pressure = pvlib.atmosphere.alt2pres(altitude) # presión a esa altitud
    am_abs = pvlib.atmosphere.get_absolute_airmass(airmass, pressure) #Deveuelve el airmass a esa altura especifica
    tl = pvlib.clearsky.lookup_linke_turbidity(times, latitude, longitude) # Factor LINKE TURBIDITY, describe el esp. óptico de la atm. por la abs. por el vapor de 
    # agua como a la abs. y disp. por las partículas de aerosol. Resume la turbidez de la atmósfera y, por tanto, la atenuación de la radiación solar directa.
    cs = pvlib.clearsky.ineichen(solpos['apparent_zenith'], am_abs, tl, dni_extra=dni_extra, altitude=altitude) # devuelve DHI (irr. horizontal), DNI Y GHI (global horizontal)
    
    """----------------ANGULO SOLAR DE INCIDENCIA E IRRADIANCIA TOTAL-------------"""
    aoi = pvlib.irradiance.aoi(s['surface_tilt'], s['surface_azimuth'],
                               solpos['apparent_zenith'], solpos['azimuth']) # Angulo solar de incidencia respecto a la superficie
    total_irrad = pvlib.irradiance.get_total_irradiance(s['surface_tilt'],s['surface_azimuth'],
                                                        solpos['apparent_zenith'], solpos['azimuth'],
                                                        cs['dni'], cs['ghi'], cs['dhi'],
                                                        dni_extra=dni_extra,model='haydavies') #  Irradiancia total= Idirecta+ Idifusa + I reflejada  (sky and ground
    
    # print("Irradiancia en la célula", i+1, "\n",round(total_irrad['poa_global'],3),"W\m^2" )
    
    """--------------AÑADO A UNIÓN DATOS--------------"""
    for x in total_irrad.index:
        if i == 0:
            union_datos.at[j,'I_sup_pv'] = total_irrad['poa_global'][j]
            j = j + 1
        elif i == 1: 
            union_datos.at[j,'I_front_pv'] = total_irrad['poa_global'][j]
            j = j + 1
        elif i == 2: 
            union_datos.at[j,'I_tras_pv'] = total_irrad['poa_global'][j]
            j = j + 1
        elif i == 3: 
            union_datos.at[j,'I_der_pv'] = total_irrad['poa_global'][j]
            j = j + 1
        elif i == 4: 
            union_datos.at[j,'I_izq_pv'] = total_irrad['poa_global'][j]
            j = j + 1
            
    i = i + 1   
    j = 0
    # union_datos.at[1,'I_sup_pv'] = total_irrad['poa_global'][i]    
    
"""------------*EXPORTAMOS UNIÓN DATOS A EXCEL*---------"""
#file_name = 'UnionDatos3.xlsx'
#union_datos.to_excel(file_name)

