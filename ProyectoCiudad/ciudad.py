import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluNewQuadric, gluCylinder, gluSphere
from OpenGL.GLU import gluPerspective, gluLookAt
import cv2 
import cv2 as cv 
import numpy as np
import math
import sys



# Variables globales para el control de la cámara
camera_yaw = 0
camera_pitch = 60  # Ángulo inicial desde arriba (60 grados)
camera_distance = 20



# Dimensiones de la ventana y matriz de puntos
window_width, window_height = 800, 600
matrix_size = 3  # Matriz fija de 3x3


# Parámetros del flujo óptico
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Coordenadas de la matriz (se llenarán dinámicamente)
fixed_points = None

# Frame anterior para el cálculo del flujo óptico
prev_gray = None



def init_fixed_points(frame_width, frame_height):
    """Inicializa los puntos de la matriz para que estén centrados en la pantalla."""
    global fixed_points
    region_width = frame_width // (matrix_size + 1)  # Espaciado entre columnas
    region_height = frame_height // (matrix_size + 1)  # Espaciado entre filas

    fixed_points = np.array(
        [[(j + 1) * region_width, (i + 1) * region_height] for i in range(matrix_size) for j in range(matrix_size)],
        dtype=np.float32
    ).reshape(-1, 1, 2)
    

def init_opengl():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_circle(radius, y, color):
    """Dibuja un círculo en el plano XZ"""
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(*color)
    glVertex3f(0, y, 0)
    for i in range(101):
        angle = 2 * math.pi * i / 100
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        glVertex3f(x, y, z)
    glEnd()

def draw_cube():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.5, 0.2)
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)
    glColor3f(0.9, 0.6, 0.3)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glColor3f(0.6, 0.4, 0.2)
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()

def draw_rectangular_prism(width, height, depth, color):
    """Dibuja un prisma rectangular con dimensiones y color especificados.

    Args:
        width: Ancho del prisma.
        height: Altura del prisma.
        depth: Profundidad del prisma.
        color: Tupla (R, G, B) que representa el color del prisma.
    """

    glColor3f(*color)  # Establece el color del prisma

    # Calcula los vértices del prisma
    x1 = -width/2
    x2 = width/2
    y1 = -height/2
    y2 = height/2
    z1 = -depth/2
    z2 = depth/2

    # Dibuja las caras del prisma utilizando GL_QUADS
    glBegin(GL_QUADS)
    # Cara frontal
    glVertex3f(x1, y1, z2)
    glVertex3f(x2, y1, z2)
    glVertex3f(x2, y2, z2)
    glVertex3f(x1, y2, z2)
    # Cara trasera
    glVertex3f(x1, y1, z1)
    glVertex3f(x2, y1, z1)
    glVertex3f(x2, y2, z1)
    glVertex3f(x1, y2, z1)
    # Cara izquierda
    glVertex3f(x1, y1, z1)
    glVertex3f(x1, y1, z2)
    glVertex3f(x1, y2, z2)
    glVertex3f(x1, y2, z1)
    # Cara derecha
    glVertex3f(x2, y1, z1)
    glVertex3f(x2, y1, z2)
    glVertex3f(x2, y2, z2)
    glVertex3f(x2, y2, z1)
    # Cara superior
    glVertex3f(x1, y2, z1)
    glVertex3f(x2, y2, z1)
    glVertex3f(x2, y2, z2)
    glVertex3f(x1, y2, z2)
    # Cara inferior
    glVertex3f(x1, y1, z1)
    glVertex3f(x2, y1, z1)
    glVertex3f(x2, y1, z2)
    glVertex3f(x1, y1, z2)
    glEnd()

def draw_house():
    """Dibuja una casa (base + techo)"""
    draw_cube()

def draw_sphere(radius, slices, stacks,color=(0, 1, 0)):
    """Dibuja una esfera usando coordenadas paramétricas."""
    glColor3f(*color)  # Establece el color de la esfera
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + i / stacks)
        z0 = radius * math.sin(lat0)
        zr0 = radius * math.cos(lat0)
        lat1 = math.pi * (-0.5 + (i + 1) / stacks)
        z1 = radius * math.sin(lat1)
        zr1 = radius * math.cos(lat1)
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * (j / slices)
            x = math.cos(lng)
            y = math.sin(lng)
            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0, y * zr0, z0)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1,
                       y * zr1, z1)
        glEnd()

def draw_tronco(radius, height, slices, stacks, color):
    """Dibuja un tronco (cilindro) de un color sólido"""

    glColor3f(*color)  # Establece el color del tronco

    for i in range(stacks):
        theta0 = float(i) * 2 * math.pi / slices
        theta1 = float(i + 1) * 2 * math.pi / slices

        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            theta = float(j) * 2 * math.pi / slices
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)

            glVertex3f(x, y, i * height / stacks)
            glVertex3f(x, y, (i + 1) * height / stacks)
        glEnd()    

def draw_camera_marker(x, y, z):
    """Dibuja un marcador en la posición de la cámara (ajustado para no obstruir la vista)."""
    glPushMatrix()
    # Mueve el marcador un poco más abajo del punto de la cámara
    glTranslatef(x, y - 1, z)
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    draw_sphere(0.01, 20, 20)  # Dibuja una esfera como marcador
    glPopMatrix()
    # Restablece el color para evitar que afecte otros objetos
    glColor3f(1.0, 1.0, 1.0)

def handle_optical_flow(camera_feed):
    """Calcula el flujo óptico y ajusta la cámara"""
    global prev_frame, camera_yaw, camera_pitch
    gray = cv2.cvtColor(camera_feed, cv2.COLOR_BGR2GRAY)
    if prev_frame is None:
        prev_frame = gray
        return
    prev_points = cv2.goodFeaturesToTrack(prev_frame, mask=None, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
    if prev_points is not None:
        curr_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_frame, gray, prev_points, None, **lk_params)
        good_old = prev_points[status == 1]
        good_new = curr_points[status == 1]
        if len(good_old) > 0:
            motion = good_new - good_old
            avg_motion = np.mean(motion, axis=0)
            camera_yaw -= avg_motion[0] * 1.0
            camera_pitch += avg_motion[1] * 1.0
            camera_pitch = max(10, min(89, camera_pitch))
    prev_frame = gray

def draw_pyramid(x, y, z, size, color):
    """
    Dibuja una pirámide centrada en las coordenadas (x, y, z) con una base cuadrada de lado 'size' y un color especificado.

    Args:
        x: Coordenada x del centro de la base de la pirámide.
        y: Coordenada y del centro de la base de la pirámide.
        z: Coordenada z del centro de la base de la pirámide.
        size: Tamaño del lado de la base de la pirámide.
        color: Tupla (R, G, B) que representa el color de la pirámide.
    """

    glBegin(GL_TRIANGLES)
    glColor3f(*color)

    # Cara frontal
    glVertex3f(x - size/2, y, z + size/2)
    glVertex3f(x + size/2, y, z + size/2)
    glVertex3f(x, y + size, z)

    # Cara trasera
    glVertex3f(x - size/2, y, z - size/2)
    glVertex3f(x + size/2, y, z - size/2)
    glVertex3f(x, y + size, z)

    # Cara izquierda
    glVertex3f(x - size/2, y, z + size/2)
    glVertex3f(x - size/2, y, z - size/2)
    glVertex3f(x, y + size, z)

    # Cara derecha
    glVertex3f(x + size/2, y, z + size/2)
    glVertex3f(x + size/2, y, z - size/2)
    glVertex3f(x, y + size, z)

    glEnd()

def draw_rectangle(x, y, width, height, color):
    """
    Dibuja un rectángulo en las coordenadas especificadas.

    Args:
        x: Coordenada x de la esquina inferior izquierda del rectángulo.
        y: Coordenada y de la esquina inferior izquierda del rectángulo.
        width: Ancho del rectángulo.
        height: Alto del rectángulo.
        color: Tupla (R, G, B) que representa el color del rectángulo.
    """

    glBegin(GL_QUADS)
    glColor3f(*color)

    # Vertices del rectángulo
    glVertex3f(x, y, 0)  # Esquina inferior izquierda
    glVertex3f(x + width, y, 0)  # Esquina inferior derecha
    glVertex3f(x + width, y + height, 0)  # Esquina superior derecha
    glVertex3f(x, y + height, 0)  # Esquina superior izquierda

    glEnd()

def draw_street():
    # Dibujar calle
    glPushMatrix()
    glTranslatef(0, 0.1, 0)
    glRotatef(-math.degrees(80.1), 1, 0, 0)
    draw_rectangle(-20, 1.5, 40, 5, (0.3, 0.3, 0.3))
    glPopMatrix()
    # Dibujar linea central calle
    for i in range(8):
        x = 0 + i * 5
        z = 0
        glPushMatrix()
        glTranslatef(x, 0.11, z)
        glRotatef(-math.degrees(80.1), 1, 0, 0)
        draw_rectangle(-20, 3.8, 2, 0.3, (0.9, 0.9, 0.9))
        glPopMatrix()

def draw_arbol():
    # dibujar un arbol
    glPushMatrix()
    glTranslatef(1.5, 3, 0)
    glRotatef(-math.degrees(80.1), 1, 0, 0)
    draw_sphere(0.6, 32, 32)
    draw_tronco(0.18, 3.0, 32, 32, (0.5, 0.2, 0))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1, 2, 0)
    glRotatef(-math.degrees(80.1), 1, 0, 0)
    draw_sphere(0.6, 32, 32)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(2, 2, 0)
    glRotatef(-math.degrees(80.1), 1, 0, 0)
    draw_sphere(0.6, 32, 32)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(1.5, 2, 0.5)
    glRotatef(-math.degrees(80.1), 1, 0, 0)
    draw_sphere(0.6, 32, 32)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(1.5, 2, -0.5)
    glRotatef(-math.degrees(80.1), 1, 0, 0)
    draw_sphere(0.6, 32, 32)
    glPopMatrix()

def draw_cube_walmart(x, y, z, width, height, depth, color):
    """Dibuja un cubo en una posición específica con dimensiones y color dados"""
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(width, height, depth)
    glColor3f(*color)
    glBegin(GL_QUADS)

    # Frente
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    # Atrás
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    # Izquierda
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    # Derecha
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)

    # Arriba
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    # Abajo
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    glEnd()
    glPopMatrix()

def draw_text_on_cube(x, y, z, text, color):
    """Dibuja texto básico simulando caracteres como líneas sobre un cubo."""
    glColor3f(*color)
    for i, char in enumerate(text):
        glPushMatrix()
        glTranslatef(x + i * 0.3, y, z)  # Posicionar cada letra
        glScalef(0.1, 0.1, 0.1)
        draw_letter(char)
        glPopMatrix()

def draw_letter(char):
    """Dibuja letras básicas como líneas simuladas (solo para algunas letras)."""
    glBegin(GL_LINES)
    if char == 'U':
        glVertex3f(-0.5, -0.5, 0.0)
        glVertex3f(-0.5, 0.5, 0.0)
        glVertex3f(0.5, -0.5, 0.0)
        glVertex3f(0.5, 0.5, 0.0)
        glVertex3f(-0.5, -0.5, 0.0)
        glVertex3f(0.5, -0.5, 0.0)
    elif char == 'A':
        glVertex3f(-0.5, -0.5, 0.0)
        glVertex3f(0.0, 0.5, 0.0)
        glVertex3f(0.5, -0.5, 0.0)
        glVertex3f(0.0, 0.5, 0.0)
        glVertex3f(-0.25, 0.0, 0.0)
        glVertex3f(0.25, 0.0, 0.0)
    elif char == 'L':
        glVertex3f(-0.5, 0.5, 0.0)
        glVertex3f(-0.5, -0.5, 0.0)
        glVertex3f(-0.5, -0.5, 0.0)
        glVertex3f(0.5, -0.5, 0.0)
    elif char == 'M':
        glVertex3f(-0.5, -0.5, 0.0)
        glVertex3f(-0.5, 0.5, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(-0.5, 0.5, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.5, 0.5, 0.0)
        glVertex3f(0.5, 0.5, 0.0)
        glVertex3f(0.5, -0.5, 0.0)
    elif char == 'R':
        glVertex3f(-0.5, -0.5, 0.0)
        glVertex3f(-0.5, 0.5, 0.0)
        glVertex3f(-0.5, 0.5, 0.0)
        glVertex3f(0.0, 0.5, 0.0)
        glVertex3f(0.0, 0.5, 0.0)
        glVertex3f(0.5, 0.0, 0.0)
        glVertex3f(-0.5, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
    elif char == 'T':
        glVertex3f(-0.5, 0.5, 0.0)
        glVertex3f(0.5, 0.5, 0.0)
        glVertex3f(0.0, 0.5, 0.0)
        glVertex3f(0.0, -0.5, 0.0)
    glEnd()

def draw_supermarket():
    # Suelo
    draw_cube_walmart(0, -0.1, 0, 20, 0.1, 20, (0.2, 0.6, 0.2))

    # Edificio principal
    draw_cube_walmart(0, 1, 0, 6, 2, 4, (0.8, 0.2, 0.2))

    # Ventanas
    draw_cube_walmart(-2, 1, 2.01, 0.8, 0.8, 0.1, (0.6, 0.8, 1.0))
    draw_cube_walmart(0, 1, 2.01, 0.8, 0.8, 0.1, (0.6, 0.8, 1.0))
    draw_cube_walmart(2, 1, 2.01, 0.8, 0.8, 0.1, (0.6, 0.8, 1.0))

    # Letrero
    draw_cube_walmart(0, 2.6, 0, 4, 0.2, 0.2, (0.0, 0.0, 0.5))
    draw_text_on_cube(-1.5, 2.6, 0.3, "UALMART", (1.0, 1.0, 1.0))

# Función para dibujar el suelo (plano)
def draw_parking_floor():
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)  # Color gris para el suelo
    glBegin(GL_QUADS)
    glVertex3f(-10, -0.1, -10)  # Esquina inferior izquierda
    glVertex3f(10, -0.1, -10)  # Esquina inferior derecha
    glVertex3f(10, -0.1, 10)  # Esquina superior derecha
    glVertex3f(-10, -0.1, 10)  # Esquina superior izquierda
    glEnd()
    glPopMatrix()


# Función para dibujar un espacio de estacionamiento
def draw_parking_space(x, y, width, depth):
    glPushMatrix()
    glTranslatef(x, 0.0, y)  # Posicionar cada espacio de estacionamiento
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro para los espacios
    glBegin(GL_QUADS)
    glVertex3f(-width / 2, 0.0, -depth / 2)
    glVertex3f(width / 2, 0.0, -depth / 2)
    glVertex3f(width / 2, 0.0, depth / 2)
    glVertex3f(-width / 2, 0.0, depth / 2)
    glEnd()
    glPopMatrix()


# Función para dibujar las líneas divisorias del estacionamiento
def draw_parking_lines():
    glPushMatrix()
    glColor3f(10.0, 5.0, 10.0)  # Color blanco para las líneas divisorias

    # Dibujar líneas divisorias entre los espacios
    glBegin(GL_LINES)

    # Líneas verticales
    for x in range(-9, 10, 2):
        glVertex3f(x, 0.0, -10)
        glVertex3f(x, 0.0, 10)

    # Líneas horizontales
    for y in range(-9, 10, 2):
        glVertex3f(-10, 0.0, y)
        glVertex3f(10, 0.0, y)

    glEnd()
    glPopMatrix()

def draw_parking():
    # Dibujar el suelo y el estacionamiento
    draw_parking_floor()  # Dibujar el suelo
    draw_parking_lines()  # Dibujar las líneas divisorias

    # Dibujar los espacios de estacionamiento (puedes modificar el número de espacios)
    for x in range(-8, 10, 4):  # Espacios de estacionamiento en X
        for y in range(-8, 10, 4):  # Espacios de estacionamiento en Y
            draw_parking_space(x, y, 2, 4)

def draw_estatua():
    # Dibuja la base de la estatua
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)  # Color gris
    glVertex3f(-1, -1, 0)
    glVertex3f(1, -1, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(-1, 1, 0)
    glEnd()

    # Dibuja el cuerpo de la estatua
    glBegin(GL_QUADS)
    glColor3f(0.7, 0.7, 0.7)  # Color gris claro
    glVertex3f(-0.5, -1, 0)
    glVertex3f(0.5, -1, 0)
    glVertex3f(0.5, 2, 0)
    glVertex3f(-0.5, 2, 0)
    glEnd()

    # Dibuja la cabeza de la estatua
    glBegin(GL_QUADS)
    glColor3f(0.9, 0.9, 0.9)  # Color gris claro
    glVertex3f(-0.2, 2, 0)
    glVertex3f(0.2, 2, 0)
    glVertex3f(0.2, 3, 0)
    glVertex3f(-0.2, 3, 0)
    glEnd()


def draw_hotdog_cart():
    # Base del carrito
    draw_cube_walmart(0, 0.5, 0, 4, 0.5, 2, (0.8, 0.2, 0.2))

    # Ruedas
    draw_cube_walmart(-1.5, 0.2, 1, 0.5, 0.5, 0.5, (0.2, 0.2, 0.2))
    draw_cube_walmart(1.5, 0.2, 1, 0.5, 0.5, 0.5, (0.2, 0.2, 0.2))
    draw_cube_walmart(-1.5, 0.2, -1, 0.5, 0.5, 0.5, (0.2, 0.2, 0.2))
    draw_cube_walmart(1.5, 0.2, -1, 0.5, 0.5, 0.5, (0.2, 0.2, 0.2))

    # Techado del carrito
    draw_cube_walmart(0, 1.5, 0, 4.2, 0.2, 2.2, (0.9, 0.9, 0.9))

    # Postes laterales
    draw_cube_walmart(-1.8, 1, 0.9, 0.1, 1.0, 0.1, (0.8, 0.8, 0.8))
    draw_cube_walmart(1.8, 1, 0.9, 0.1, 1.0, 0.1, (0.8, 0.8, 0.8))
    draw_cube_walmart(-1.8, 1, -0.9, 0.1, 1.0, 0.1, (0.8, 0.8, 0.8))
    draw_cube_walmart(1.8, 1, -0.9, 0.1, 1.0, 0.1, (0.8, 0.8, 0.8))

    # Parrilla del carrito
    draw_cube_walmart(0, 1.0, 0, 3.8, 0.1, 1.8, (0.5, 0.5, 0.5))

    # Manija trasera del carrito
    draw_cube_walmart(-2.2, 1.0, 0, 0.2, 0.5, 0.1, (0.3, 0.3, 0.3))
    draw_cube_walmart(-2.2, 1.25, 0, 0.2, 0.1, 1.2, (0.3, 0.3, 0.3))

    # Hot dogs sobre la parrilla
    draw_cube_walmart(-0.5, 1.1, 0.5, 0.8, 0.2, 0.2, (0.8, 0.4, 0.1))
    draw_cube_walmart(0.5, 1.1, 0.5, 0.8, 0.2, 0.2, (0.8, 0.4, 0.1))
    draw_cube_walmart(0, 1.1, -0.5, 0.8, 0.2, 0.2, (0.8, 0.4, 0.1))

def draw_semaforo():
    # dibujar semaforo
    glPushMatrix()
    glTranslatef(0, 3, 0)
    draw_rectangular_prism(0.5, 2, 0.5, (0, 0, 0))
    glPopMatrix()
    # luz 1
    glPushMatrix()
    glTranslatef(0.26, 3.8, 0)
    glRotatef(90, 0, 0, 1)
    draw_circle(0.18, 0, (0, 1, 0))
    glPopMatrix()
    # luz 2
    glPushMatrix()
    glTranslatef(0.26, 3.33, 0)
    glRotatef(90, 0, 0, 1)
    draw_circle(0.18, 0, (1, 1, 0))
    glPopMatrix()
    # luz 3
    glPushMatrix()
    glTranslatef(0.26, 2.8, 0)
    glRotatef(90, 0, 0, 1)
    draw_circle(0.18, 0, (1, 0, 0))
    glPopMatrix()
    # poste
    glPushMatrix()
    glTranslatef(-0.16, 2, 0)
    glRotatef(90, 1, 0, 0)
    draw_tronco(0.15, 2, 10, 10, (0, 0, 0))
    glPopMatrix()

def draw_carro():
    # Base del carro (cuerpo principal en amarillo)
    draw_cube_walmart(0, 0.5, 0, 6, 0.5, 3, (1.0, 1.0, 0.0))  # Color amarillo

    # Ruedas
    draw_cube_walmart(-2.5, 0.25, 1.5, 0.5, 0.5, 0.5, (0.1, 0.1, 0.1))  # Frontal izquierda
    draw_cube_walmart(2.5, 0.25, 1.5, 0.5, 0.5, 0.5, (0.1, 0.1, 0.1))   # Frontal derecha
    draw_cube_walmart(-2.5, 0.25, -1.5, 0.5, 0.5, 0.5, (0.1, 0.1, 0.1)) # Trasera izquierda
    draw_cube_walmart(2.5, 0.25, -1.5, 0.5, 0.5, 0.5, (0.1, 0.1, 0.1))  # Trasera derecha

    # Ventanas laterales
    draw_cube_walmart(0, 1.5, 1.4, 5.5, 0.4, 0.1, (0.5, 0.8, 1.0))  # Lateral derecha
    draw_cube_walmart(0, 1.5, -1.4, 5.5, 0.4, 0.1, (0.5, 0.8, 1.0)) # Lateral izquierda

    # Luces frontales
    draw_cube_walmart(-2, 0.7, 1.6, 0.4, 0.4, 0.1, (1, 1, 0))  # Izquierda
    draw_cube_walmart(2, 0.7, 1.6, 0.4, 0.4, 0.1, (1, 1, 0))   # Derecha

    # Luces traseras
    draw_cube_walmart(-2, 0.7, -1.6, 0.4, 0.4, 0.1, (1, 0, 0)) # Izquierda
    draw_cube_walmart(2, 0.7, -1.6, 0.4, 0.4, 0.1, (1, 0, 0))  # Derecha

def draw_stop_sign():
    # Color rojo para la señal
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glBegin(GL_POLYGON)
    for i in range(8):
        angle = math.radians(i * 45)  # 360/8 = 45 grados
        x = 1.0 * math.cos(angle)
        y = 1.0 * math.sin(angle)
        glVertex3f(x, y, 0)  # Vértices del octágono
    glEnd()

    # Opcional: dibujar un borde blanco alrededor de la señal
    glColor3f(1.0, 1.0, 1.0)  # Blanco
    glBegin(GL_LINE_LOOP)
    for i in range(8):
        angle = math.radians(i * 45)  # 360/8 = 45 grados
        x = 1.0 * math.cos(angle)
        y = 1.0 * math.sin(angle)
        glVertex3f(x, y, 0.01)  # Vértices del borde
    glEnd()

def draw_post():
    # Poste de la señal
    glColor3f(1, 1, 1)  # Color gris
    glBegin(GL_QUADS)
    glVertex3f(-0.05, -1, 0)  # Esquina inferior izquierda
    glVertex3f(0.05, -1, 0)   # Esquina inferior derecha
    glVertex3f(0.05, 1, 0)    # Esquina superior derecha
    glVertex3f(-0.05, 1, 0)   # Esquina superior izquierda
    glEnd()

def draw_stop():
    # dibujar senal de stop
    glPushMatrix()
    glTranslatef(-3, 5, 0)
    draw_stop_sign()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-3, 3, 0)
    draw_post()
    glPopMatrix() 
def draw_farola():
    # Factor de escala para reducir el tamaño a la mitad
    escala = 0.5

    # Dibujar el poste de la farola
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)
    glRotatef(-90, 1, 0, 0)
    glTranslate(0,0,0)
    glScalef(escala, escala, escala)  # Aplicamos la escala
    gluCylinder(gluNewQuadric(), 0.2, 0.2, 10.0 * escala, 32, 32)
    glPopMatrix()

    # Dibujar el brazo de la farola
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)
    glTranslate(0,-2,0)
    glTranslatef(0.0, 8.0 * escala, 0.0)
    glRotatef(90, 0, 1, 0)
    glScalef(escala, escala, escala)
    gluCylinder(gluNewQuadric(), 0.2, 0.2, 2.0 * escala, 32, 32)
    glPopMatrix()

    # Dibujar el foco (lámpara)
    glPushMatrix()
    glColor3f(1.0, 1.0, 0.0)
    glTranslate(-0.5,-2,0)
    glTranslatef(2.0 * escala, 8.0 * escala, 0.0)
    glScalef(escala, escala, escala)
    gluSphere(gluNewQuadric(), 0.5 * escala, 32, 32)
    glPopMatrix()

    # Dibujar la base de la farola
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)
    glTranslatef(0.0, -0.5 * escala, 0.0)
    glRotatef(-90, 1, 0, 0)
    glScalef(escala, escala, escala)
    gluCylinder(gluNewQuadric(), 0.5 * escala, 0.7 * escala, 0.5 * escala, 32, 32)
    glPopMatrix()
       
def draw_scene():
    """Dibuja toda la escena"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # Configuración de la cámara
    camera_x = camera_distance * math.cos(math.radians(camera_yaw)) * math.cos(math.radians(camera_pitch))
    camera_z = camera_distance * math.sin(math.radians(camera_yaw)) * math.cos(math.radians(camera_pitch))
    camera_y = camera_distance * math.sin(math.radians(camera_pitch))
    gluLookAt(camera_x, camera_y, camera_z, 0, 0, 0, 0, 1, 0)
    # Dibujar el suelo
    draw_circle(30, 0, (0.55, 0.55, 0.55))
    draw_street()
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glRotatef(-math.degrees(80.1), 0, 1, 0)
    draw_street()
    glPopMatrix()
    # Dibujar casas
    for i in range(8):
        if i == 4:
            continue
        else:
            angle = 0
            x = -15 + i * 5
            z = 0
            glPushMatrix()
            glTranslatef(x, 0, z)
            glRotatef(-math.degrees(angle), 0, 1, 0)
            draw_house()
            glPopMatrix()
    for i in range(8):
        if i == 4:
            continue
        else:
            angle = 0
            x = -15 + i * 5
            z = 8
            glPushMatrix()
            glTranslatef(x, 0, z)
            glRotatef(-math.degrees(angle), 0, 1, 0)
            draw_house()
            glPopMatrix()
    # dibujar techos
    for i in range(8):
        if i == 4:
            continue
        else:
            x=-15.5 + i*5
            glPushMatrix()
            glTranslatef(x, 0.5, 0)
            glRotatef(-math.degrees(angle), 0, 1, 0)
            draw_pyramid(0.5, 0.5, 0, 2, (0.1, 0.1, 0.1))
            glPopMatrix()
    for i in range(8):
        if i == 4:
            continue
        else:
            x=-15.5 + i*5
            z=8
            glPushMatrix()
            glTranslatef(x, 0.5, z)
            glRotatef(-math.degrees(angle), 0, 1, 0)
            draw_pyramid(0.5, 0.5, 0, 2, (0.2, 0.2, 0.2))
            glPopMatrix()
    for i in range(1):
        x=-3.6 + i*5
        glPushMatrix()
        glTranslatef(x, 0, 1)
        draw_arbol()
        glPopMatrix()

    # dibujar edificios
    glPushMatrix()
    glTranslatef(-0.5, 4.5, -5)
    draw_rectangular_prism(3,8,5,(0,0,0))
    glPopMatrix()

    # dibujar walmart
    glPushMatrix()
    glTranslatef(9, 0, 13)
    glRotatef(90, 0, 1, 0)
    draw_supermarket()
    glPopMatrix()
    # dibujar farolas
    glPushMatrix()
    glTranslatef(1.3, 0.01, 1)
    draw_farola()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(6.8, 0.01, 1)
    glRotatef(-180, 0, 1, 0)
    draw_farola()
    glPopMatrix()
    # dibujar stacionamiento
    glPushMatrix()
    glTranslatef(-12,1,20)
    draw_parking()
    glPopMatrix()
    # dibujar farolas
    glPushMatrix()
    glTranslatef(1.3, 0.01, 7)
    draw_farola()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(6.8, 0.01, 7)
    glRotatef(-180, 0, 1, 0)
    draw_farola()
    glPopMatrix()
    # dibujar stacionamiento
    glPushMatrix()
    glTranslatef(-12,1,20)
    draw_parking()
    glPopMatrix()

    # dibujar estatua
    glPushMatrix()
    glTranslatef(-8,0.5, 18)
    draw_estatua()
    glPopMatrix()
    # Dibujar carrito hotdogs
    glPushMatrix()
    glTranslatef(10,1,-5)
    draw_hotdog_cart()
    glPopMatrix()
    # dibujar semaforo
    glPushMatrix()
    glTranslatef(1,0,1.5)
    draw_semaforo()
    glPopMatrix()
    # dibujar carro
    glPushMatrix()
    glTranslatef(3, 1, 4)
    draw_carro()
    glPopMatrix()
    # Dibujar el marcador de la cámara
    draw_camera_marker(camera_x, camera_y, camera_z)
    glfw.swap_buffers(window)
    #dibujar stop
    glPushMatrix()
    glTranslatef ( 2, 3, 3)
    draw_stop()
    glPopMatrix()
    
    


def process_optical_flow(frame):
    global prev_gray, camera_yaw, camera_distance, camera_pitch

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_gray is None:
        prev_gray = gray
        return

    # Calcular el flujo óptico
    new_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, fixed_points, None, **lk_params)

    for i, (new, old) in enumerate(zip(new_points, fixed_points)):
        if status[i]:
            dx, dy = new.ravel() - old.ravel()
            if abs(dx) > 3 or abs(dy) > 3:  # Detectar movimiento significativo
                if i == 0:
                    camera_yaw -= 2
                elif i == 2:
                    camera_yaw += 2
                elif i == 6:
                    camera_distance = max(5, camera_distance - 0.5)
                elif i == 8:
                    camera_distance = min(30, camera_distance + 0.5)

    prev_gray = gray


def draw_matrix_on_camera(frame):
    """Dibuja la matriz de puntos en la ventana de la cámara"""
    for point in fixed_points:
        x, y = point.ravel()
        cv2.circle(frame, (int(x), int(y)), 10, (0, 255, 0), -1)


def main():
    
    
    global window
    if not glfw.init():
        sys.exit()
    window = glfw.create_window(800, 600, "Proyecto final", None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)
    glViewport(0, 0, 800, 600)
    init_opengl()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        sys.exit()

    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el frame de la cámara.")
        sys.exit()

    init_fixed_points(frame.shape[1], frame.shape[0])  # Inicializar matriz centrada

    if not glfw.init():
        sys.exit()

    window = glfw.create_window(window_width, window_height, "Escena 3D", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, window_width, window_height)
    init_opengl()

    while not glfw.window_should_close(window):
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Voltear la imagen para una experiencia más intuitiva

        draw_matrix_on_camera(frame)  # Dibujar la matriz de puntos
        process_optical_flow(frame)  # Procesar flujo óptico

        cv2.imshow("Cámara", frame)  # Mostrar la ventana de la cámara
        draw_scene()  # Dibujar la escena 3D

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        glfw.poll_events()
    cap.release()
    glfw.terminate()

if __name__ == "__main__":
    main()