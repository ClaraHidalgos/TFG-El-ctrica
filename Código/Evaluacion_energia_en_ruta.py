import pvlib
from datetime import datetime
from datetime import timedelta
import pandas as pd
import osmnx as ox 
import requests
import math

""" PASO 4: Añadir las caras del vehículo (superficies inclinadas)
    •	Reflejar las diferentes orientaciones de los paneles solares. Divide el vehículo en caras:
        o	Techo: Horizontal o ligeramente inclinado.
        o	Laterales (izquierdo y derecho): Ángulos específicos dependiendo del diseño.
        o	Frontal y trasera: Con inclinaciones más pronunciadas.
    •	Para cada cara:
        o	Define la inclinación (tilt) y orientación (azimuth).
        o	Calcula la irradiancia recibida con get_total_irradiance.
    •	Suma las contribuciones de todas las caras para obtener la generación total del vehículo.

"""


def calcular_angulos_y_areas(angulo):
    """
    Esta función toma un ángulo y genera un DataFrame que contiene:
    - Las transformaciones de los ángulos (tilt y azimuth) correspondientes a cinco caras de un vehículo.
    - El área de cada cara.

    Parámetros:
    ----------
    angulo : float
        Ángulo azimuth inicial (dirección principal del vehículo, en grados).

    Retorno:
    --------
    df : pandas.DataFrame
        DataFrame con las columnas ['theta_z', 'theta_t', 'area'] que representan el azimuth,
        tilt y área para las cinco caras del vehículo.
    """
    df = pd.DataFrame(columns=['theta_z', 'theta_t', 'area'], index=range(1, 6))
    
    # Áreas calculadas para cada cara (en m²)
    areas = {
        1: 2.94,  # Techo
        2: 1.53,  # Frontal
        3: 0.49,  # Trasera
        4: 2.68,  # Lateral derecha
        5: 2.68   # Lateral izquierda
    }
    
    # CARA SUPERIOR
    df.loc[1, 'theta_z'] = 0  # Azimuth
    df.loc[1, 'theta_t'] = 0  # Tilt 
    df.loc[1, 'area'] = areas[1]
    
    # CARA FRONTAL
    df.loc[2, 'theta_z'] = angulo
    df.loc[2, 'theta_t'] = 15
    df.loc[2, 'area'] = areas[2]
    
    # CARA TRASERA
    if angulo < 180:
        df.loc[3, 'theta_z'] = angulo + 180
    else:
        df.loc[3, 'theta_z'] = angulo - 180
    df.loc[3, 'theta_t'] = 30
    df.loc[3, 'area'] = areas[3]
    
    # CARA LATERAL DERECHA
    if angulo < 270:
        df.loc[4, 'theta_z'] = angulo + 90
    else:
        df.loc[4, 'theta_z'] = angulo - 270
    df.loc[4, 'theta_t'] = 90
    df.loc[4, 'area'] = areas[4]
    
    # CARA LATERAL IZQUIERDA
    if angulo < 90:
        df.loc[5, 'theta_z'] = angulo + 270
    else:
        df.loc[5, 'theta_z'] = angulo - 90
    df.loc[5, 'theta_t'] = 90
    df.loc[5, 'area'] = areas[5]
    
    return df


def calcular_azimuth(lat1, lon1, lat2, lon2):
    """
    Calcula el azimuth/rumbo entre dos puntos dados por su latitud y longitud.
    
    Parámetros:
    -----------
    lat1, lon1: Coordenadas del primer punto (en grados).
    lat2, lon2: Coordenadas del segundo punto (en grados).
    
    Retorno:
    --------
    azimuth: El azimuth/rumbo en grados (en el rango [0, 360)).
    """
    # Convertir coordenadas a radianes
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    delta_lon = lon2 - lon1

    # Calcular rumbo usando la fórmula del azimuth
    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    azimuth = math.atan2(x, y)

    # Convertir rumbo de radianes a grados y ajustarlo al rango [0, 360)
    azimuth = math.degrees(azimuth)
    azimuth = (azimuth + 360) % 360

    return azimuth

def obtener_altitud(lat, lon, altitudes):
    try:
        # Intentar obtener la altitud desde la API
        url = f"https://api.opentopodata.org/v1/srtm90m?locations={lat},{lon}"
        response = requests.get(url)
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]['elevation']
    except:
        pass  # Si falla, sigue a la estrategia de respaldo
    
    # Si no se encontró altitud, usar el valor anterior o la media
    if len(altitudes) > 0:
        # Obtener último valor válido que no sea 0
        valores_validos = [alt for alt in altitudes if alt > 0]
        if len(valores_validos) > 0:
            return valores_validos[-1]  # Usar último válido
        else:
            return 373  # Altitud promedio por defecto para Madrid
    else:
        return 373  # Valor predeterminado inicial


# Función para calcular la irradiancia total de todas las caras del vehículo
def calcular_energia_vehiculo(lat, lon, alt, time, angulo , svf, albedo, tiempo ):
    # Obtener ángulos tilt y azimuth para cada cara
    angulos = calcular_angulos_y_areas(angulo) 

    # Parámetros del sistema fotovoltaico
    eficiencia = 0.18
    
    # Convertir time a DatetimeIndex
    time = pd.DatetimeIndex([time])
    
    # Inicializar energía total
    energia_total = 0
    
    # Crear un dataframe para almacenar los resultados por cara
    columnas = ['Cara', 'Area', 'E_total', 'E_directa', 'E_difusa', 'E_reflejada']
    resultados = pd.DataFrame(columns=columnas)

    # Iterar sobre las caras del vehículo
    for i in range(1, 6):  # Del 1 al 5 (caras)
    # Obtención de los ángulos 
        tilt = angulos['theta_t'][i]  # Inclinación de la cara i
        azimuth = angulos['theta_z'][i]  # Orientación de la cara i
        
        # Calcular irradiancia en la cara: posición del sol, La radiación extraterrestre y linke_turbidity
        solpos = pvlib.solarposition.get_solarposition(time, lat, lon)
        dni_extra = pvlib.irradiance.get_extra_radiation(time)
        linke_turbidity = pvlib.clearsky.lookup_linke_turbidity(time, lat, lon)

    # Modelo de cielo despejado 
        cs = pvlib.clearsky.ineichen(
            solpos['apparent_zenith'],
            pvlib.atmosphere.get_absolute_airmass(
                pvlib.atmosphere.get_relative_airmass(solpos['apparent_zenith']),
                pvlib.atmosphere.alt2pres(alt)
            ),
            linke_turbidity,
            dni_extra=dni_extra,
            altitude=alt
        )
        # Irradiancia en la cara i
        poa = pvlib.irradiance.get_total_irradiance(
            surface_tilt=tilt,
            surface_azimuth=azimuth,
            dni=cs['dni'],
            ghi=cs['ghi'],
            dhi=cs['dhi'],
            solar_zenith=solpos['apparent_zenith'],
            solar_azimuth=solpos['azimuth'],
            albedo=albedo,
            model='perez',
            dni_extra =dni_extra
        )
      
        poa.reset_index(drop=True, inplace=True)  # Eliminar el índice basado en fechas
        
        # Calculo de la energia inicial sin svf
        if  i == 1:
            E_inicial = poa * eficiencia * angulos['area'][i] * (tiempo / 3600) 
        else:
            E = poa * eficiencia * angulos['area'][i] * (tiempo / 3600) 
            E_inicial = pd.concat([E_inicial, E], ignore_index=True)
            
        # Ajustar la componente difusa por el SVF dependiendo de la inclinación
        if tilt == 0:  # Techo
           poa['poa_diffuse'] *= svf
        elif tilt == 90:  # Laterales
            poa['poa_diffuse'] *= svf * 0.5
        else:  # Frontal y trasera
            poa['poa_diffuse'] *= svf * (1 - tilt / 90)
         
        # Calculo de la energía con el svf
        if  i == 1:
            E_final = poa * eficiencia * angulos['area'][i] * (tiempo / 3600) 
        else:
            E = poa * eficiencia * angulos['area'][i] * (tiempo / 3600) 
            E_final = pd.concat([E_final, E], ignore_index=True)
        
        # Procesamiento de la energía por componentes
        E_directa = poa['poa_direct'][0] * eficiencia * angulos['area'][i]  * (tiempo / 3600)  # Wh
        E_difusa = poa['poa_diffuse'][0] * eficiencia * angulos['area'][i]  * (tiempo / 3600)  # Wh
        E_reflejada = poa['poa_ground_diffuse'][0] * eficiencia * angulos['area'][i]  * (tiempo / 3600)  # Wh
        E_total = E_directa + E_difusa + E_reflejada
        
        # Añadir los datos de esta cara al dataframe de resultados
        resultados = pd.concat([
            resultados,
            pd.DataFrame({
                'Cara': [i],
                'Area': angulos['area'][i],
                'E_total': [E_total],
                'E_directa': [E_directa],
                'E_difusa': [E_difusa],
                'E_reflejada': [E_reflejada]
            })
        ], ignore_index=True)
        
        
    return E_final, E_inicial, resultados



# Nombre de los archivos con los puntos y los SVF de la ruta y unión de eellos
nombres_archivos = ["puntos2_oliva1.xlsx", "puntos2_oliva2.xlsx"]
# Cargar los archivos en DataFrames
dataframes = []
for i, archivo in enumerate(nombres_archivos):
    df = pd.read_excel(archivo)
    # Eliminar la última fila del primer y segundo archivo
    if i < len(nombres_archivos) - 1:  # Si no es el último archivo
        df = df.iloc[:-1]  # Elimina la última fila
    dataframes.append(df)
# Concatenar los DataFrames
puntos = pd.concat(dataframes, ignore_index=True)

# Parámetros del sistema FV
albedo = 0.2  # Albedo típico
eficiencia = 0.18  # Eficiencia del sistema
velocidad = 35 * 1000 / 3600  # Velocidad en m/s (30 km/h)
puntos['SVF_teorico'] = 0.5

# Inicialización de variables
hora_inicial = pd.Timestamp("2024-05-04 14:00:00", tz='Europe/Madrid') # Inicializar tiempo inicial
energia_total = 0
energia_total_teorico = 0
energia_tramo_teorico = 0
energia_tramo = 0
puntos["altitud"] = 0  # Agregar columna para altitud
puntos["hora"] = hora_inicial
altitudes = []  # Lista para almacenar las altitudes calculadas
tabla_acumulada = None
distancia_total = 0
tiempo_total = 0

# Iterar sobre los puntos
for i in range(1, len(puntos)):
    lat1, lon1 = puntos.loc[i-1, ["coor_y", "coor_x"]]
    lat2, lon2 = puntos.loc[i, ["coor_y", "coor_x"]]
    angulo = calcular_azimuth(lat1, lon1, lat2, lon2)
    svf = puntos.loc[i, "SVF %"]/100

    # Obtener altitud, usando el respaldo si no se encuentra
    puntos.loc[i, "altitud"] = obtener_altitud(lat2, lon2, altitudes)

    # Agregar la altitud calculada a la lista
    altitudes.append(puntos.loc[i, "altitud"])

    # Calcular distancia y tiempo entre puntos
    distancia = ox.distance.euclidean(lat1, lon1, lat2, lon2) * 100000
    tiempo = distancia / velocidad
    #print(tiempo)
    puntos.loc[i, "hora"] = puntos.loc[i-1, "hora"] + timedelta(seconds=tiempo)
    print(f"Distancia: {distancia:.2f} m, Tiempo: {tiempo:.2f} s, SVF: {svf}")
    # Calcular irradiancia y energía generad
    E_final, E_inicial, resultados = calcular_energia_vehiculo(lat1, lon1, puntos.loc[i, "altitud"], puntos.loc[i, "hora"], angulo , svf, albedo, tiempo )
    E_final_suma = pd.DataFrame([E_final.sum(axis=0)], columns=E_final.columns)
    E_inicial_suma = pd.DataFrame([E_inicial.sum(axis=0)], columns=E_inicial.columns)
    
    # Calculo de t y distancia:
    distancia_total += distancia
    tiempo_total += tiempo  
    
    # Si la tabla acumulada no existe, inicializarla con los valores actuales
    if tabla_acumulada is None:
        tabla_acumulada = resultados.copy()
    else:
        # Sumar los valores actuales a la tabla acumulada
        tabla_acumulada['E_total'] += resultados['E_total']
        tabla_acumulada['E_directa'] += resultados['E_directa']
        tabla_acumulada['E_difusa'] += resultados['E_difusa']
        tabla_acumulada['E_reflejada'] += resultados['E_reflejada']
    
    if i==1:
        E_final_global = E_final_suma.copy()
        E_inicial_global = E_inicial_suma.copy()
        
    else:
        E_final_global = pd.concat([E_final_global, E_final_suma.copy()], ignore_index=True) 
        E_inicial_global = pd.concat([E_inicial_global, E_inicial_suma.copy()], ignore_index=True) 
    

# Mismo proceso pero con SVF teórico    
for i in range(1, len(puntos)):
    lat1, lon1 = puntos.loc[i-1, ["coor_y", "coor_x"]]
    lat2, lon2 = puntos.loc[i, ["coor_y", "coor_x"]]
    angulo = calcular_azimuth(lat1, lon1, lat2, lon2)
    svf = puntos.loc[i, "SVF_teorico"]

    # Agregar la altitud calculada a la lista
    altitudes.append(puntos.loc[i, "altitud"])
    # Calcular distancia y tiempo entre puntos
    distancia = ox.distance.euclidean(lat1, lon1, lat2, lon2) * 100000
    tiempo = distancia / velocidad

    E_final_t, E_inicial_t, res = calcular_energia_vehiculo(lat1, lon1, puntos.loc[i, "altitud"], puntos.loc[i, "hora"], angulo , svf, albedo, tiempo )
    E_final_suma_t = pd.DataFrame([E_final_t.sum(axis=0)], columns=E_final_t.columns)
    E_inicial_suma_t = pd.DataFrame([E_inicial_t.sum(axis=0)], columns=E_inicial_t.columns)
    
    if i==1:
        E_final_global_t = E_final_suma_t.copy()
        E_inicial_global_t = E_inicial_suma_t.copy()
        
    else:
        E_final_global_t = pd.concat([E_final_global_t, E_final_suma_t.copy()], ignore_index=True) 
        E_inicial_global_t = pd.concat([E_inicial_global_t, E_inicial_suma_t.copy()], ignore_index=True) 
      
        

tabla_acumulada.to_excel("Resultados_Oliva.xlsx")
E_final_global_t.to_excel("E_final_global_t_Oliva.xlsx")
E_inicial_global.to_excel("E_inicial_global_Oliva.xlsx")
E_final_global.to_excel("E_final_global_Oliva.xlsx")



