import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluNewQuadric, gluPerspective, gluCylinder, gluSphere
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

def draw_farola():
    # Limpiar la pantalla y preparar la matriz de transformación
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Mover la cámara para ver la farola
    glTranslatef(0.0, -1.5, -20)  # Mover la cámara hacia atrás para ver la farola

    # Dibujar el poste de la farola
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)  # Color gris para el poste
    glRotatef(-90, 1, 0, 0)  # Rotar para alinear el cilindro verticalmente
    gluCylinder(gluNewQuadric(), 0.2, 0.2, 10.0, 32, 32)  # Poste alto y delgado
    glPopMatrix()

    # Dibujar el brazo de la farola
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)  # Mismo color para el brazo
    glTranslatef(0.0, 8.0, 0.0)  # Subir el brazo hacia la parte superior del poste
    glRotatef(90, 0, 1, 0)  # Rotar para alinear el cilindro horizontalmente
    gluCylinder(gluNewQuadric(), 0.2, 0.2, 2.0, 32, 32)  # Brazo horizontal
    glPopMatrix()

    # Dibujar el foco (lámpara)
    glPushMatrix()
    glColor3f(1.0, 1.0, 0.0)  # Color amarillo para representar luz
    glTranslatef(2.0, 8.0, 0.0)  # Posicionar el foco al final del brazo
    gluSphere(gluNewQuadric(), 0.5, 32, 32)  # Esfera pequeña para el foco
    glPopMatrix()

    # Dibujar la base de la farola
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)  # Color oscuro para la base
    glTranslatef(0.0, -0.5, 0.0)  # Colocar la base debajo del poste
    glRotatef(-90, 1, 0, 0)  # Rotar para que quede horizontal
    gluCylinder(gluNewQuadric(), 0.5, 0.7, 0.5, 32, 32)  # Base del poste
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
    window = glfw.create_window(width, height, "Farola", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_farola()     # Dibujar la farola
        glfw.poll_events()     # Procesar eventos

    glfw.terminate()

if __name__ == "__main__":
    main()