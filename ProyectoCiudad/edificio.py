import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image, ImageEnhance
import os
import sys

# Variables globales
window = None
texture_id_building = None  # ID de textura para las paredes
texture_id_roof = None      # ID de textura para el techo

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
        return None

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
    """Inicializa las texturas del edificio y el techo"""
    global texture_id_building, texture_id_roof
    texture_id_building = load_texture("C:\\Users\\Angel Alipio\\Desktop\\mr_yosie\\alcarajo.jpg")  # Reemplaza con la ruta de la textura de las paredes
    texture_id_roof = load_texture("C:\\Users\\Angel Alipio\\Desktop\\mr_yosie\\pared.jpg")      # Reemplaza con la ruta de la textura del techo

    if texture_id_building is None or texture_id_roof is None:
        print("Error: No se pudieron cargar las texturas.")
        sys.exit()

def draw_building():
    """Dibuja un edificio texturizado"""
    if texture_id_building is None or texture_id_roof is None:
        print("Error: No se han cargado las texturas necesarias.")
        return

    # Dibujar las paredes del edificio con la textura de paredes
    glEnable(GL_TEXTURE_2D)
    
    glBegin(GL_QUADS)
    # Cara frontal
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.0, 1.0)
    # Cara trasera
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.0, -1.0)
    # Cara izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.0, -1.0)
    # Cara derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.0, 1.0, -1.0)
    glEnd()

    # Dibujar el techo del edificio con la textura de techo
    glBindTexture(GL_TEXTURE_2D, texture_id_roof)
    glBegin(GL_QUADS)
    # Cara superior (techo)
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.0, -1.0)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def draw_scene():
    """Dibuja toda la escena"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(5, 5, 10,  # Posición de la cámara
              0, 0, 0,   # Punto al que mira
              0, 1, 0)   # Vector hacia arriba

    # Dibujar el edificio
    glPushMatrix()
    glTranslatef(0, 0, 0)  # Posición del edificio
    draw_building()
    glPopMatrix()

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Edificio Texturizado con Techo", None, None)
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
        draw_scene()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "_main__":
    main()