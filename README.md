Repositorio que recoje el código y documentos usados para realizar el TFG. Este se compone de 3 partes:
  1. Realización de un anlcaje para unir el sensor al cualquier coche y poder hacer campañas de medición.
  2. Calibración del sensor. Para esto hay que medir en el mediodía solar y comparar las medidas tomadas con las de la estación del IES. Después,
    hay que cambiar las costantes de los distintos sensores para su posterior uso. Para el procesamiento de datos se va a usar pyhton.
  3. Código en python con ayuda de pvlib para la realización de campañas de medida. Se va a reultilizar parte del código del punto 2.

Para hacer toda la parte de código se van a usar 3 archivos de datos distintas. Primero, los datos obtenido en la estación de medición del IES que
nos van a ayudar a calibrar el sensor y nos van a dar datos para poder simular con Pvlib como la temperatura del ambiente o velocidad del viento.
Segundo, vamos a usar los datos tomados con los sensores, los cuales se van subiendo a ThingSpeak. Por último, se va a simular en PvLib las mismas 
situaciones en las que se va a encontrar el sensor en las campañas de medidas.
