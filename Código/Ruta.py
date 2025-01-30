import networkx as nx
import osmnx as ox
import math
import numpy as np
import utm
import pandas as pd
ox.__version__
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt

# Función para detectar intersecciones
def es_interseccion(node, G):
    """
    Determina si un nodo es una intersección en el grafo, basado en el número de conexiones.

    Args:
        node (int): El nodo a evaluar.
        G (networkx.MultiDiGraph): El grafo en el que se encuentra el nodo.

    Returns:
        bool: Verdadero si el nodo es una intersección, Falso en caso contrario.
    """
    degree = G.degree(node)
    return degree >= 3  # Se considera intersección si tiene al menos 3 conexiones

def filtrar_intersecciones(route, intersecciones, G, distancia_min=40):
    """
    Filtra las intersecciones en función de la distancia total en la ruta entre ellas.
    
    Args:
        route (list): Lista de nodos en la ruta.
        intersecciones (list): Lista de nodos de intersección.
        G (graph): Grafo de la red de calles.
        distancia_min (float): Distancia mínima en metros entre intersecciones.
    
    Returns:
        list: Lista de intersecciones filtradas.
    """
    intersecciones_filtradas = [intersecciones[0]]  # Comienza con la primera intersección

    for i in range(len(intersecciones) - 1):
        # Encuentra los índices de las intersecciones en la ruta
        index_ini = route.index(intersecciones[i])
        index_fin = route.index(intersecciones[i + 1])
        
        # Calcula la distancia acumulada en el tramo entre estas dos intersecciones
        distancia_acumulada = 0
        for j in range(index_ini, index_fin):
            nodo_actual = route[j]
            nodo_siguiente = route[j + 1]
            distancia_acumulada += ox.distance.euclidean_dist_vec(
                G.nodes[nodo_actual]['y'], G.nodes[nodo_actual]['x'],
                G.nodes[nodo_siguiente]['y'], G.nodes[nodo_siguiente]['x']
            )*100000

        # Si la distancia acumulada es mayor o igual que el umbral, guarda la intersección
        if distancia_acumulada >= distancia_min:
            intersecciones_filtradas.append(intersecciones[i + 1])

    return intersecciones_filtradas

def ruta(dist, origen, destino ):
    """
    Determina los puntos de una ruta, dado una distncia entre puntos, u origen y un destino. Además de detectar las interecciones
    en la ruta y seleccioarlas según interese o no

    Args:
        dist (int): distancia entre puntos.
        
        origen (list): latitud y longitud del inicio de la ruta.
        destino (list): latitud y longitud del final de la ruta.
    Returns:
        DataFrame:  donde vienen los puntos determinados por la longitud y la latirud.
    """
    
    
    # DISTANCIA DE INTERPOLACIÓN
    DIST_MIN = dist
    RADIO_TIERRA = 6371000
    
    # PUNTO DE SALIDA L0: longitud; LA: latitud
    LO1 = origen[1]
    LA1 = origen[0]
    # PUNTO DE LLEGADA L0: longitud; LA: latitud
    LO2 = destino[1]
    LA2 = destino[0]
    
    
    # Hacemos más grande el mapa para asegurarnos que la ruta que se genere esté dentro
    if LA1 >= LA2:
        north= LA1 + 0.01
        south = LA2 - 0.01
    else:
        north= LA1 - 0.01
        south = LA2 + 0.01
        
    if LO1 >= LO2:
        east = LO1 + 0.01
        west = LO2 - 0.01
        
    else: 
        east = LO1 - 0.01
        west = LO2 + 0.01
    
    
    # CREAMOS EL MAPA:  
    G_aux = ox.graph.graph_from_bbox(north, south, east, west, simplify=False, retain_all=True, network_type='drive')
    #fig2, ax2 = ox.plot_graph(G_aux)
    
    
    # Buscamos los nodos más cercanos de las coordenadas de salida y llegada
    orig = ox.distance.nearest_nodes(G_aux, X = LO1, Y = LA1  )
    dest = ox.distance.nearest_nodes(G_aux, X = LO2, Y=  LA2 )
    
    
    # Se crea la ruta dentro del mapa 
    route_aux = ox.shortest_path(G_aux, orig, dest, weight="travel_time")
    #fig4, ax4 = ox.plot_graph_route(G_aux, route_aux, node_size=0)
    
    # Identificar intersecciones y puntos intermedios en la ruta
    intersections = [node for node in route_aux if es_interseccion(node, G_aux)]
    intersections_filtradas = filtrar_intersecciones(route_aux, intersections, G_aux)
    
    
    # Creamos un array para guardar la distancia en linea recta entre dos coordenadas
    dist = np.zeros(shape= len(route_aux)-1)
    dist_2 = np.zeros(shape= len(route_aux)-1)
    
    # Cálculo de la distancia entre dos interecciones, para ello hay que pasar todas las coordenadas a
    # utm y tener la aporximación en x e y, teneindo en cuenta que hay que hay que ir sumando los tramos por linea reacta
    for i in range(0, len(intersections_filtradas)-1):
        index_ini = route_aux.index(intersections_filtradas[i])
        index_fin = route_aux.index(intersections_filtradas[i+1])
        dist_2 = 0
        for j in range(index_fin-index_ini):
            dist_1 = ox.distance.euclidean_dist_vec(G_aux._node[route_aux[index_ini + j]]['y'], 
            G_aux._node[route_aux[index_ini + j]]['x'], G_aux._node[route_aux[index_ini + j+1]]['y'], 
            G_aux._node[route_aux[index_ini + j+1]]['x'])*100000
            dist_2 = dist_1+dist_2
        
        dist[i] = dist_2
        
        
    # Una vez obtenidos las distancias entre nodos principales (intersección entre calles), se va a 
    # a interpolar entre estos nodos principlales cada Xm, teniendo en cuenta TODOS los nodos que nos
    # devuelve la ruta si no simplificamos, es decir, vamos a interpolar con puntos que forman rectas. 
    # Se itera sobre los nodos auxiliares para encontrar puntos a intervalos regulares.
    
    puntos = pd.DataFrame(columns=['coor_y', 'coor_x', 'nodo'])
    dist_2 = np.zeros(shape=1)
    
    
    for i in range(len(intersections_filtradas)):
        if dist[i] < DIST_MIN:
            puntos = puntos.append({'coor_y': G_aux._node[intersections_filtradas[i]]['y'], 'coor_x':G_aux._node[intersections_filtradas[i]]['x'], 'nodo': 1}, ignore_index=True)
            
        
        elif dist[i] > DIST_MIN:
            # El primer punto es el nodo de la ruta normal que coincidirá con el rpimer punto de la ruta auxiliar
            puntos = puntos.append({'coor_x': G_aux._node[intersections_filtradas[i]]['x'], 'coor_y':G_aux._node[intersections_filtradas[i]]['y'], 'nodo': 1}, ignore_index=True)
            index_ini = route_aux.index(intersections_filtradas[i])
            index_fin = route_aux.index(intersections_filtradas[i+1])
            dist_2 = np.zeros(shape = index_fin-index_ini)
            #resto = 0
            resto2=0
            # recorremos los nodos de la ruta auxiliar entre dos nodos contiguos de la ruta normal
            for j in range(index_fin-index_ini):
                
                # Cálculo de la distancia entre nodos auxiliares 
                coor_utm_1 = utm.from_latlon(G_aux._node[route_aux[index_ini + j]]['y'], G_aux._node[route_aux[index_ini + j]]['x'])
                coor_utm_2 = utm.from_latlon(G_aux._node[route_aux[index_ini + j+1]]['y'], G_aux._node[route_aux[index_ini + j+1]]['x'])
                dist_lat = abs(coor_utm_1[0]-coor_utm_2[0])
                dist_lon = abs(coor_utm_1[1]-coor_utm_2[1])
                distancia = math.sqrt((dist_lat*dist_lat)+(dist_lon*dist_lon))
                dist_2[j] = distancia
            
                
                if (distancia+resto2)<DIST_MIN:
                    resto2=distancia+resto2
                    
                else: 
                    # puntos de la recta siendo x1 el inicial
                    x1_pend = coor_utm_1[1] 
                    y1_pend = coor_utm_1[0] 
                    x2_pend = coor_utm_2[1]
                    y2_pend = coor_utm_2[0]
                    
                    pendiente = (y2_pend-y1_pend)/(x2_pend-x1_pend)  
                    # pendiente2 = (y1_pend-y2_pend)/(x1_pend-x2_pend)
                    # Definimos la pedneinte de la recta
                    """if x1_pend <= x2_pend:
                        pendiente = pendiente1
                    elif x1_pend> x2_pend:
                        pendiente = pendiente2"""
                   
                    # Empezamos a buscar puntos a 10 m
                    
                    # El primer punto entre dos nodos de route es el primero
                    if j==0:
                        # puntos = puntos.append({'coor_x': G._node[route[i]]['x'], 'coor_y':G._node[route[i]]['y']}, ignore_index=True)
                        x1 = coor_utm_1[1] # x
                        y1 = coor_utm_1[0] # y
                        
                     
                        # Iteramos cada 10m, es decir, la distancia 
                    for k in range(round(((distancia+resto2)/DIST_MIN)+0.5)+1):
                        # El primer punto corresponde con el del nodo inicial, es decir, x1 e y1
                        if k == 0:
                            a = 1 + (pendiente**2)
                            b = (-2*x1_pend)-(2*x1_pend*(pendiente**2))
                            c = -((DIST_MIN-resto2)**2)+(x1_pend**2) + ((pendiente*x1_pend)**2)
                            
                            x_sol_1 = (-b-math.sqrt((-4*a*c)+(b*b)))/(2*a)
                            y_sol_1 = pendiente*(x_sol_1-x1_pend) + y1_pend
                            x_sol_2 = (-b+math.sqrt((-4*a*c)+(b*b)))/(2*a)
                            y_sol_2 = pendiente*(x_sol_2-x1_pend) + y1_pend
                
                            distancia_sol_1 = math.sqrt(((abs(y1_pend-y_sol_1))**2)+((abs(x1_pend-x_sol_1))**2))
                            distancia_sol_2 = math.sqrt(((abs(y1_pend-y_sol_2))**2)+((abs(x1_pend-x_sol_2))**2))
                            
                            if x1_pend <= x2_pend:
                                if x_sol_1 >= x1_pend:
                                    x1 = x_sol_1
                                    y1 = y_sol_1
                                elif x_sol_2 > x1_pend:
                                    x1 = x_sol_2
                                    y1 = y_sol_2
                                    
                            elif x1_pend > x2_pend:
                                if x_sol_1 <= x1_pend:
                                    x1 = x_sol_1
                                    y1 = y_sol_1
                                elif x_sol_2 < x1_pend:
                                    x1 = x_sol_2
                                    y1 = y_sol_2
        
                            resto2 = distancia + resto2 - DIST_MIN
                            cooordenadas = utm.to_latlon(y1, x1, coor_utm_1[2], coor_utm_1[3])
                            puntos = puntos.append({'coor_y': cooordenadas[0], 'coor_x': cooordenadas[1]}, ignore_index=True)
                        
                        # Si la distancia entre nodos ya es menor de 10 salimos y vamos a por el siguiente
                        elif resto2 < DIST_MIN:
                            break
                        
                        elif resto2>DIST_MIN:
                            a = 1 + (pendiente**2)
                            b = (-2*x1)-(2*x1*(pendiente**2))
                            c = -((DIST_MIN)**2)+(x1**2) + ((pendiente*x1)**2)
                            x_sol_1 = (-b-math.sqrt((-4*a*c)+(b*b)))/(2*a)
                            y_sol_1 = pendiente*(x_sol_1-x1) + y1
                            x_sol_2 = (-b+math.sqrt((-4*a*c)+(b*b)))/(2*a)
                            y_sol_2 = pendiente*(x_sol_2-x1) + y1
                            
                            
                            distancia_sol_1 = math.sqrt(((abs(y2_pend-y_sol_1))**2)+((abs(x2_pend-x_sol_1))**2))
                            distancia_sol_2 = math.sqrt(((abs(y2_pend-y_sol_2))**2)+((abs(x2_pend-x_sol_2))**2))
                            
                            if distancia_sol_1 < ((distancia-(k+1)*DIST_MIN) + 1 + resto2):
                                x1 = x_sol_1
                                y1 = y_sol_1
                            elif distancia_sol_2 < ((distancia-(k+1)*DIST_MIN) + 1 + resto2):
                                x1 = x_sol_2
                                y1 = y_sol_2
                                
                            resto2 = resto2 - DIST_MIN
                            cooordenadas = utm.to_latlon(y1, x1, coor_utm_1[2], coor_utm_1[3])
                            puntos = puntos.append({'coor_y': cooordenadas[0], 'coor_x': cooordenadas[1]}, ignore_index=True)
                        
                       
            #for k in range(round(dist[i]/DIST_MIN)):
    
                
    # DIBUJAMOS LOS PUNTOS EN EL MAPA
    
    # Añadir nodos de intersección en rojo y nodos intermedios en azul
    # Visualizar la ruta con intersecciones y puntos intermedios resaltados
    fig, ax = ox.plot_graph_route(G_aux, route_aux, node_size=0, show=False, close=False)
    
    pos = {node: (G_aux.nodes[node]['x'], G_aux.nodes[node]['y']) for node in route_aux}
    
    nx.draw_networkx_nodes(G_aux, pos=pos, nodelist=intersections, node_color="red", node_size=30, ax=ax, label="Intersecciones")
    nx.draw_networkx_nodes(G_aux, pos=pos, nodelist=intersections_filtradas, node_color="blue", node_size=15, ax=ax, label="Puntos intermedios")
        
    plt.legend(loc="upper right")
    plt.show()

    #puntos.to_excel('puntos2.xlsx')     
    
    return puntos
    