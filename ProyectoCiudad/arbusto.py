import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluNewQuadric, gluSphere, gluPerspective, gluCylinder
import sys

# Variables globales
window = None

def init():
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo de color azul
    glEnable(GL_DEPTH_TEST)            # Activar prueba de profundidad
    glEnable(GL_LIGHTING)              # Activar iluminación
    glEnable(GL_LIGHT0)                # Activar la luz 0

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.0, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    # Configuración de la luz
    light_pos = [1.0, 1.0, 1.0, 1.0]  # Posición de la luz
    light_color = [1.0, 1.0, 1.0, 1.0]  # Color de la luz blanca
    ambient_light = [0.2, 0.2, 0.2, 1.0]  # Luz ambiental

    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)

def draw_arbusto():
    # Limpiar la pantalla y preparar la matriz de transformación
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Mover la cámara para ver el arbusto
    glTranslatef(0.0, -1.0, -30)  # Mover la cámara hacia atrás para ver el arbusto

    # Cambiar el color de las hojas a verde
    material_diffuse_hojas = [0.0, 0.4, 0.0, 1.0]  # Color verde para las hojas
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse_hojas)

    # Dibujar las esferas (hojas del arbusto) en verde

    glPushMatrix()
    glTranslatef(0.1, 0.9, 1.5)  # Posición de una esfera en la parte trasera
    gluSphere(gluNewQuadric(), 1.5, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 3.0, 0.0)  # Posición de una esfera superior
    gluSphere(gluNewQuadric(), 1.5, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(2.0, 2.0, 0.0)  # Posición de una esfera lateral
    gluSphere(gluNewQuadric(), 1.5, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-2.0, 2.0, 1)  # Posición de otra esfera lateral
    gluSphere(gluNewQuadric(), 1.5, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.5, 0.0, 0.9)  # Posición de una esfera en la parte trasera
    gluSphere(gluNewQuadric(), 1.5, 32, 32)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.1, 0.0, 1)  # Posición de una esfera en la parte inferior
    gluSphere(gluNewQuadric(), 1.5, 32, 32)
    glPopMatrix()

    # Cambiar el color del tronco a café (marrón)
    material_diffuse_tronco = [0.6, 0.3, 0.1, 1.0]  # Color marrón/café para el tronco
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse_tronco)

    # Dibujar el tronco del arbusto (cilindro)
    glPushMatrix()
    glTranslatef(0.0, -0.8, 0.0)  # Colocar el tronco en la base del arbusto
    glRotatef(90, 1, 0, 0)  # Rotar el tronco para que quede vertical
    gluCylinder(gluNewQuadric(), 0.5, 0.5, 4.0, 32, 32)  # Crear el cilindro
    glPopMatrix()

    # Intercambiar buffers para mostrar el resultado
    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 500, 500
    window = glfw.create_window(width, height, "Arbusto Estático", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_arbusto()         # Dibujar el arbusto (con hojas y tronco)
        glfw.poll_events()    # Procesar eventos

    glfw.terminate()

if __name__ == "__main__":
    main()