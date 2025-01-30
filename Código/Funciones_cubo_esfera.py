import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Use Tkinter backend
from mpl_toolkits.mplot3d.art3d import Poly3DCollection



def generar_esfera_3d(imagen_front_re, imagen_top_re, imagen_back_re, imagen_rface_re, imagen_lface_re, TAMANO, ax):
    """
    Genera la proyección de 5 imágenes en una semiesfera 3D, devolviendo los vértices de la esfera y renderizando la imagen en 3D.
    
    Args:
        imagen_front_re (array): Imagen de la cara frontal
        imagen_top_re (array): Imagen de la cara superior
        imagen_back_re (array): Imagen de la cara trasera
        imagen_rface_re (array): Imagen de la cara derecha
        imagen_lface_re (array): Imagen de la cara izquierda
        TAMANO (int): Tamaño de la cuadrícula que define los pequeños cuadrados de la semiesfera
        ax (matplotlib.axes._subplots.Axes3DSubplot)
    Returns:
        sphere_vertices: Lista de vértices proyectados en la esfera
    """

    # Crear una lista para almacenar los vértices de la esfera y sus colores
    sphere_vertices = []
    sphere_col_dec = []


    k = 0  # Contador para los cuadrados

    for i in range(TAMANO):
        for j in range(TAMANO):
            # ----- Proyectar la cara superior -----
            # Definir los vértices de un cuadrado en la cara superior
            x_top = np.linspace(-1 + 2 * j / TAMANO, -1 + 2 * (j + 1) / TAMANO, 2)
            y_top = np.linspace(-1 + 2 * (i) / TAMANO, -1 + 2 * (i + 1) / TAMANO, 2)
            z_top = [1] * 2  # Z es constante en la cara superior
            square_top = [[x_top[0], y_top[0], z_top[0]], [x_top[0], y_top[1], z_top[0]],
                          [x_top[1], y_top[1], z_top[0]], [x_top[1], y_top[0], z_top[0]]]

            # Proyectar el cuadrado en la esfera
            sphere_vertices_front = [vertex / np.linalg.norm(vertex) for vertex in square_top]
            sphere_vertices.append(np.array(sphere_vertices_front))

            # Obtener el color del cuadrado desde la imagen correspondiente
            col = np.array([imagen_top_re[j][i][2], imagen_top_re[j][i][1], imagen_top_re[j][i][0], 255])
            col_dec = col / 255
            sphere_col_dec.append(col_dec)

            # Añadir el cuadrado a la visualización 3D
            ax.add_collection3d(Poly3DCollection([sphere_vertices_front], color=col_dec, edgecolors=None))
            k += 1

            # ----- Proyectar la cara derecha -----
            x_right = np.linspace(1 - 2 * i / TAMANO, 1 - 2 * (i + 1) / TAMANO, 2)
            y_right = [1] * 2
            z_right = np.linspace(1 - 2 * j / TAMANO, 1 - 2 * (j + 1) / TAMANO, 2)
            if z_right[0] >= 0 and z_right[1] >= 0:  # Verificar si la coordenada Z es no negativa
                square_right = [[x_right[0], y_right[0], z_right[0]], [x_right[1], y_right[1], z_right[0]],
                                [x_right[1], y_right[1], z_right[1]], [x_right[0], y_right[0], z_right[1]]]

                sphere_vertices_right = [vertex / np.linalg.norm(vertex) for vertex in square_right]
                sphere_vertices.append(np.array(sphere_vertices_right))

                col = np.array([imagen_rface_re[j][i][2], imagen_rface_re[j][i][1], imagen_rface_re[j][i][0], 255])
                col_dec = col / 255
                sphere_col_dec.append(col_dec)
                ax.add_collection3d(Poly3DCollection([sphere_vertices_right], color=col_dec, edgecolors=None))

            # ----- Proyectar la cara izquierda -----
            x_left = np.linspace(-1 + 2 * i / TAMANO, -1 + 2 * (i + 1) / TAMANO, 2)
            y_left = [-1] * 2
            z_left = np.linspace(1 - 2 * j / TAMANO, 1 - 2 * (j + 1) / TAMANO, 2)
            if z_left[0] >= 0 and z_left[1] >= 0:  # Verificar si la coordenada Z es no negativa
                square_left = [[x_left[0], y_left[0], z_left[0]], [x_left[1], y_left[1], z_left[0]],
                               [x_left[1], y_left[1], z_left[1]], [x_left[0], y_left[0], z_left[1]]]

                sphere_vertices_left = [vertex / np.linalg.norm(vertex) for vertex in square_left]
                sphere_vertices.append(np.array(sphere_vertices_left))

                col = np.array([imagen_lface_re[j][i][2], imagen_lface_re[j][i][1], imagen_lface_re[j][i][0], 255])
                col_dec = col / 255
                sphere_col_dec.append(col_dec)
                ax.add_collection3d(Poly3DCollection([sphere_vertices_left], color=col_dec, edgecolors=None))

            # ----- Proyectar la cara frontal -----
            x_front = [1] * 2
            y_front = np.linspace(-1 + 2 * i / TAMANO, -1 + 2 * (i + 1) / TAMANO, 2)
            z_front = np.linspace(1 - 2 * (j) / TAMANO, +1 - 2 * (j + 1) / TAMANO, 2)
            if z_front[0] >= 0 and z_front[1] >= 0:  # Verificar si la coordenada Z es no negativa
                square_front = [[x_front[0], y_front[0], z_front[0]], [x_front[1], y_front[1], z_front[0]],
                                [x_front[1], y_front[1], z_front[1]], [x_front[0], y_front[0], z_front[1]]]

                sphere_vertices_front = [vertex / np.linalg.norm(vertex) for vertex in square_front]
                sphere_vertices.append(np.array(sphere_vertices_front))

                col = np.array([imagen_front_re[j][i][2], imagen_front_re[j][i][1], imagen_front_re[j][i][0], 255])
                col_dec = col / 255
                sphere_col_dec.append(col_dec)
                ax.add_collection3d(Poly3DCollection([sphere_vertices_front], color=col_dec, edgecolors=None))

            # ----- Proyectar la cara trasera -----
            x_back = [-1] * 2
            y_back = np.linspace(1 - 2 * (i) / TAMANO, 1 - 2 * (i + 1) / TAMANO, 2)
            z_back = np.linspace(1 - 2 * (j) / TAMANO, 1 - 2 * (j + 1) / TAMANO, 2)
            if z_back[0] >= 0 and z_back[1] >= 0:  # Verificar si la coordenada Z es no negativa
                square_back = [[x_back[0], y_back[0], z_back[0]], [x_back[1], y_back[1], z_back[0]],
                               [x_back[1], y_back[1], z_back[1]], [x_back[0], y_back[0], z_back[1]]]

                sphere_vertices_back = [vertex / np.linalg.norm(vertex) for vertex in square_back]
                sphere_vertices.append(np.array(sphere_vertices_back))

                col = np.array([imagen_back_re[j][i][2], imagen_back_re[j][i][1], imagen_back_re[j][i][0], 255])
                col_dec = col / 255
                sphere_col_dec.append(col_dec)
                ax.add_collection3d(Poly3DCollection([sphere_vertices_back], color=col_dec, edgecolors=None))
            
            # Set limits and labels
            ax.set_xlim([-1, 1])
            ax.set_ylim([-1, 1])
            ax.set_zlim([0, 1])  # Limitando la visualización a la parte superior de la esfera
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')


    return sphere_vertices,  sphere_col_dec, ax  # Devolver los vértices de la esfera proyectados


def proyectar_equisolida(vertices, radio=1):
    """
    Proyecta los vértices de un cuadrado en 3D (en una semiesfera) al plano XY
    usando una proyección equisólida.
    
    Args:
        vertices: array de vértices en 3D (n, 3)
        radio: radio de la semiesfera (por defecto 1)
        
    Returns:
        Proyección 2D de los vértices (n, 2)
    """
    proyeccion = []
    
    for vertice in vertices:
        x, y, z = vertice
        # Proyección equisólida al plano z = 0
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arctan2(np.sqrt(x**2 + y**2), z)
        x_proy = x / r * np.sin(theta)
        y_proy = y / r * np.sin(theta)
        proyeccion.append([x_proy, y_proy])
    
    return np.array(proyeccion)