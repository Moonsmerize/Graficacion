import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import cv2
import numpy as np
import math
import sys

# Variables globales para el control de la cámara
camera_yaw = 0
camera_pitch = 60  # Ángulo inicial desde arriba (60 grados)
camera_distance = 20

# Variables de flujo óptico
prev_frame = None
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

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

def draw_rectangular_prism(width, height, depth, color=(1, 0, 0)):
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
            glVertex3f(x * zr1, y * zr1, z1)
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
            camera_yaw -= avg_motion[0] * 0.5
            camera_pitch += avg_motion[1] * 0.5
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
    
    # Dibujar el marcador de la cámara
    draw_camera_marker(camera_x, camera_y, camera_z)
    glfw.swap_buffers(window)

def main():
    global window
    if not glfw.init():
        sys.exit()
    window = glfw.create_window(800, 600, "Flujo Óptico con OpenCV", None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)
    glViewport(0, 0, 800, 600)
    init_opengl()
    cap = cv2.VideoCapture(0)
    while not glfw.window_should_close(window):
        ret, frame = cap.read()
        if ret:
            handle_optical_flow(frame)
        draw_scene()
        glfw.poll_events()
    cap.release()
    glfw.terminate()

if __name__ == "__main__":
    main()