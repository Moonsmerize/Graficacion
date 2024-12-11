import cv2
import numpy as np
import random

# Configuración de la ventana
width, height = 800, 600
window_name = 'Pelota Rebotando'

# Inicializa la ventana
cv2.namedWindow(window_name)

# Parámetros de la pelota
ball_radius = 20
ball_x = random.randint(ball_radius, width - ball_radius)
ball_y = random.randint(ball_radius, height - ball_radius)
ball_speed_x = 5
ball_speed_y = 5

# Función para generar un color aleatorio
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Color inicial de la pelota
ball_color = random_color()

while True:
    # Crea una imagen negra
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Dibuja la pelota
    cv2.circle(img, (ball_x, ball_y), ball_radius, ball_color, -1)

    # Muestra la imagen
    cv2.imshow(window_name, img)

    # Actualiza la posición de la pelota
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Verifica colisiones con los bordes
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= width:
        ball_speed_x = -ball_speed_x  # Cambia la dirección en el eje X
        ball_color = random_color()  # Cambia el color

    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= height:
        ball_speed_y = -ball_speed_y  # Cambia la dirección en el eje Y
        ball_color = random_color()  # Cambia el color

    # Espera 30 ms y verifica si se presiona la tecla 'q' para salir
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Cierra todas las ventanas
cv2.destroyAllWindows()