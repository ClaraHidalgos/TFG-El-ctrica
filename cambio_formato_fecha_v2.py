import pandas as pd
import matplotlib.pyplot as plt
import pvlib





"""DESCRIPCIÓN: programa que coje la fecha y la hora proporcionada por ThinkSpeak y la convierte al tipo de datos que
necesitamos, es decir,  de: 2022-02-22T15:27:45+01:00 a	2022-02-22 15:27:45 """

def cambio_formato_fecha(file_TS1):

   for i in file_TS1.index:
       a = file_TS1['Fecha'][i].replace('T', ' ') # Eliminamos la T
       b = a[:-6] # Eliminamos los 6 últimos parámetros, que son los que corresponden a la zona horaria
       file_TS1.at[i, 'Fecha'] = b
   
   return file_TS1['Fecha']       
       

"""DESCRIPCIÓN: coge 2022-02-22 15:27:45  y lo cambia al formato horario donde estamos y al tipo de dato, es decir, 
Timestamp('2022-02-22 15:27:45+0100', tz='Europe/Madrid') """
def cambio_datatime(times, zona_horaria, timezone_carroof):
    i = 0
    for x in times.index:
        rep = times[x].replace(tzinfo = None)
        times[x] = rep.tz_localize(zona_horaria).tz_convert(timezone_carroof)
   
    times = pd.DatetimeIndex(times)

    return times

            
"""DESCRIPCIÓN: la función pvlib.solarposition.get_solarposition en su primer parametro solo acepta un tipo
de datos pandas.DatetimeIndex y nosotros solo le queremos meter un elemento no un datatime, con lo que tenemos
que hacer que el elemento de times se convierta en un datatime de tamaño1"""
def time_to_tl(times):
    df = pd.Series(data = 1,index = range(1))
    df[0] = times
    df = pd.DatetimeIndex(df) 
    return df