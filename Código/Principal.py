import cv2

#LIBRERÍAS PROPIAS
import Obt_fot_maps
import Ruta
import Procesamiento_imagenes
import os


nombre_carpeta = 'Ruta_centro_madrid4'
# Creación de la carpeta


# ORIGEN Y DESTINO DE LA RUTA Y DISTANCIA ENTRE PUNTOS
distancia = 200

origen =  [37.8849253,	-6.5879744]
destino = [37.88798,	-6.5773329]



# OBTENCIÓN DE LOS PUNTOS DE A RUTA CON SUS COORDENADAS
puntos_ruta = Ruta.ruta(distancia, origen, destino)
print("Hola, mundo!1\n")

 
#puntos=pd.read_excel("puntos2.xlsx")
#puntos=puntos.drop(['Unnamed: 0'], axis=1)


i = 0
#  OBTENCIÓN DE LAS 5 FOTOS POR CADA COORDENADA
for y in puntos_ruta.coor_y:
    Obt_fot_maps.fotos(puntos_ruta.coor_y[i],puntos_ruta.coor_x[i], i, nombre_carpeta)
    i = i+1


# UNIÓN DE LAS 5 FOTOS

# PROCESADO DE LAS IMÁGENES
vector_fsv = Procesamiento_imagenes.imagenes(nombre_carpeta, puntos_ruta.shape[0])

puntos_ruta['SVF (%)'] = vector_fsv

puntos_ruta.to_excel(nombre_carpeta+'/puntos2.xlsx')    



cv2.waitKey(0)
cv2.destroyAllWindows()






    
    
    