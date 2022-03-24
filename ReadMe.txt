Carpeta donde se incluye el programa de cálculo de la irradiancia global en cada cara del sensor. El programa principal
es "coche_en_movimiento.py". El resto de programas hay una descripción al inicio de lo que hacen. Explicado a groso modo,
son funciones que ayudan al programa pricipal y hace que éste último no sea tan dificil de entender y tan engorroso.

Dentro del programa principal, "coche_en_movimiento.py" se van a abirir 3 archivos:
	file_TS1_1 -> corresponde al canal 1 de ThingSpeak. Ahora mismo está modificado con lo que no serviría si te lo descargas directamente.
	file_TS2 -> corresponde al canal 2 de ThingSpeak. Dentro de pd.read_excel hay que poner el nombre del archivo pero primero hay que 
	modificarle con estos pasos:
		1. Nos descargaos el archivo de ThingSpeak.
		2. Lo abrimos
		3. Pinchamos en la clumna A seleccionar todo.
		4. Nos vamos a 'Datos' y después pinchamos en 'Texto en columnas'
		5. En la primera ventana damos a 'Siguiente >'
		6. En la segunda en 'Separadores' seleccionamos unicamente 'Coma' y deseleccionamos 'Tabulación'. Después damos a 'Siguiente >'
		7. En la tercera en 'Avanzadas' en 'Separador Decimal' pongo "." y en 'Separador de miles' pongo "'" y damos a finalizar
		8. Nos aseguramos de que el excel creado solo llegue hasta 'Field7' el rest de columnas a su derecha se deben eliminar.
		9. Guardamos el archivo como .xlsx y con el nombre que queramos
	file_meteo_junto-> corresponde a los datos de la estación meteorológica. No hace falta cambiar el nombre ni nada, solamente poner el 
	nombre dentro de "pd.read_csv()"

Después hay que modificar dentro del programa más datos. En """ZONA HORARIA, MÓDULO E INVERSOR""" tenemos 6 parametros que habrá que cambiar.
	1. zona_horaria-> hay que poner la zona horaria de donde se estén haciendo las mediciones PEROOOO OJOOO:  hay que cambiar el + por el -
	. Por ejemplo, la zona horaria de Madrid es 'Etc/GMT+1' pues habría que poner 'Etc/GMT-1'.
	2. sandia_modules-> NO IMPORTA PORQUE SE USA PARA EL CÁLCULO DE ENERGÍA
	3. sapm_inverters-> NO IMPORTA PORQUE SE USA PARA EL CÁLCULO DE ENERGÍA
	4. module-> dentro de "sandia_modules" hay que poner el nombre de los modulos fotovoltaicos con los que se está trabajadno 
	5. inverter-> dentro de "sapm_inverters" hay que poner el nombre del inversor que se está usando

FINALMENTE: el programa nos devuelve un excel donde la primera fila 'A' es el número de dato empezando por 0, la segunda 'B' corresponde a fecha y hora, 
la tercera 'C' a la temperatura del aire ,la cuarta 'D' a la velocidad del aire en m/S, la quinta'E' a la latitud, la sexta 'F' a la longitud y la 
séptima 'G' a la altitud. Después en grupos de 4 columnas, con un total de 5 grupos corresponidentes cada uno a una cara del coche, es decir,
a un sensor distinto. La primera columna corresponde al azimuth de esa cara, la segunda a su inclinación, la tercera a la irradiancia recibida 
calculada por pvlib y la cuarta la irraciancia recibida medida por el sensor.