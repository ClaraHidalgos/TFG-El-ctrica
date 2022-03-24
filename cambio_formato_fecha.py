import pandas as pd
import matplotlib.pyplot as plt
import pvlib

"""DESCRIPCIÓN: programa que coje la fecha y la hora proporcionada por ThinkSpeak y la convierte al tipo de datos que
necesitamos, es decir,  de: 2022-02-22T15:27:45+01:00 a	2022-02-22 15:27:45-01:00. Así pvlib a la hora de calcular
la irradiancia acepta el formato"""
def cambio_formato_fecha(file_TS1):

    i = 0
    #file_TS1 = pd.read_excel('datos_22_02_22.xlsx')
    
    for x in file_TS1.index:
        a = file_TS1['Fecha'][i].replace('T', ' ')
        if file_TS1['Fecha'][i][19] == '-':
            b = a.replace('-', 'l', True)
            c = b.replace('-', 'j', True)
            d = c.replace('-', '+')
            e = d.replace('l', '-')
            f = e.replace('j', '-')
        elif file_TS1['Fecha'][i][19] == '+':
            b = a.replace('-', 'l', True)
            c = b.replace('-', 'j', True)
            d = c.replace('+', '-')
            e = d.replace('l', '-')
            f = e.replace('j', '-')
        else:
            print("Revisar el formato de hora, no es l correcto, debe ser año-mes-diaThora:minutos:segundoszonahoraria\n")
            
        file_TS1.at[i, 'Fecha'] = f

        i = i + 1
    
        
    return  file_TS1


def cambio_datatime(times, zona_horaria):
    i = 0
    
    for x in times.index:
        rep = times[i].replace(tzinfo= None)
        times[i]=rep.tz_localize(zona_horaria)
        i = i+1
    
    times = pd.DatetimeIndex(times) 
    
    return times
            

def time_to_tl(times, zona_horaria):
    df = pd.Series(data = 1,index = range(1))
    df[0] = times
    df[0] = df[0].replace(tzinfo= None)
    df[0] = df[0].tz_localize(zona_horaria)
    df = pd.DatetimeIndex(df) 
    return df