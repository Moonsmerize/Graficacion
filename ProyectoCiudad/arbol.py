import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image, ImageEnhance
import os
import sys
import math

# Variables globales
window = None
texture_id_hojas = None  # ID de textura para las hojas
texture_id_tronco = None  # ID de textura para el tronco

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)

def load_texture(image_path):
    """Cargar una imagen como textura"""
    if not os.path.exists(image_path):
        print(f"Error: El archivo {image_path} no se encuentra.")
        return None  # Devuelve None si el archivo no se encuentra

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Cargar imagen
    image = Image.open(image_path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    # Ajustar brillo
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.7)

    img_data = image.convert("RGB").tobytes()

    # Configuración de textura
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture

def initialize_textures():
    """Inicializa las texturas de las hojas y del tronco"""
    global texture_id_hojas, texture_id_tronco
    texture_id_hojas = load_texture("arbusto.jpg")  # Actualiza la ruta
    texture_id_tronco = load_texture("tronco.jpg")  # Actualiza la ruta de la textura del tronco
    if texture_id_hojas is None or texture_id_tronco is None:
        print("Error: No se pudo cargar las texturas.")
        sys.exit()  # Terminar el programa si las texturas no se cargan

def draw_sphere(radius, slices, stacks):
    """Dibuja una esfera con la textura de las hojas sin gluSphere"""
    if texture_id_hojas is None:
        print("Error: No se ha cargado la textura de las hojas.")
        return

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id_hojas)  # Usar textura de hojas

    # Parametros de la esfera
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + float(i) / stacks)  # Latitud inferior
        lat1 = math.pi * (-0.5 + float(i + 1) / stacks)  # Latitud superior
        z0 = math.sin(lat0)
        z1 = math.sin(lat1)
        r0 = math.cos(lat0)
        r1 = math.cos(lat1)

        glBegin(GL_TRIANGLE_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * float(j) / slices  # Longitud
            x = math.cos(lng)
            y = math.sin(lng)

            # Coordenadas de la esfera
            glTexCoord2f(float(j) / slices, float(i) / stacks)  # Coordenada de textura
            glVertex3f(x * r0 * radius, y * r0 * radius, z0 * radius)
            glTexCoord2f(float(j) / slices, float(i + 1) / stacks)
            glVertex3f(x * r1 * radius, y * r1 * radius, z1 * radius)
        glEnd()

    glDisable(GL_TEXTURE_2D)

def draw_tronco(radius, height, slices, stacks):
    """Dibuja un tronco (cilindro) con textura"""
    if texture_id_tronco is None:
        print("Error: No se ha cargado la textura del tronco.")
        return

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id_tronco)  # Usar textura del tronco

    # Dibujar el tronco como un cilindro
    for i in range(stacks):
        theta0 = float(i) * 2 * math.pi / slices
        theta1 = float(i + 1) * 2 * math.pi / slices

        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            theta = float(j) * 2 * math.pi / slices
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)

            # Coordenadas de textura
            u = float(j) / slices
            v0 = float(i) / stacks
            v1 = float(i + 1) / stacks

            glTexCoord2f(u, v0)
            glVertex3f(x, y, i * height / stacks)
            glTexCoord2f(u, v1)
            glVertex3f(x, y, (i + 1) * height / stacks)
        glEnd()

    glDisable(GL_TEXTURE_2D)

def draw_arbusto():
    """Dibuja el arbusto con hojas y tronco"""
    # Limpiar la pantalla y preparar la matriz de transformación
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Mover la cámara para ver el arbusto
    glTranslatef(0.0, -1.0, -30)  # Mover la cámara hacia atrás para ver el arbusto

    # Dibujar las esferas (hojas del arbusto) con textura de hojas
    glPushMatrix()
    glTranslatef(0.1, 0.9, 1.5)  # Posición de una esfera en la parte trasera
    draw_sphere(1.5, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 3.0, 0.0)  # Posición de una esfera superior
    draw_sphere(1.5, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(2.0, 2.0, 0.0)  # Posición de una esfera lateral
    draw_sphere(1.5, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-2.0, 2.0, 1)  # Posición de otra esfera lateral
    draw_sphere(1.5, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.5, 0.0, 0.9)  # Posición de una esfera en la parte trasera
    draw_sphere(1.5, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.1, 0.0, 1)  # Posición de una esfera en la parte inferior
    draw_sphere(1.5, 32, 32)
    glPopMatrix()

    # Dibujar el tronco del arbusto con textura
    material_diffuse_tronco = [0.6, 0.3, 0.1, 1.0]  # Color marrón/café para el tronco
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse_tronco)

    # Dibujar el tronco del arbusto (cilindro) con textura
    glPushMatrix()
    glTranslatef(0.0, -0.8, 0.0)  # Colocar el tronco en la base del arbusto
    glRotatef(90, 1, 0, 0)  # Rotar el tronco para que quede vertical
    draw_tronco(0.5, 4.0, 32, 32)  # Crear el tronco con textura
    glPopMatrix()

    # Intercambiar buffers para mostrar el resultado
    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Arbusto con textura de hojas y tronco", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Inicializar las texturas
    initialize_textures()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_arbusto()  # Dibujar el arbusto con las esferas y el tronco
        glfw.poll_events()  # Procesar eventos

    glfw.terminate()

if __name__ == "__main__":
    main()