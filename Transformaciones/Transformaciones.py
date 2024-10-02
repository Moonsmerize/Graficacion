# subir commit como: Actividad 1 Commit

import cv2 as cv
import numpy as np
import math

# Cargar la imagen

img = cv.imread('download.png', 0)

# Obtener el tamaño de la imagen
x, y = img.shape

# Crear una imagen vacía
rotated_img = np.zeros((x*2, y*2), dtype=np.uint8)

xx, yy = rotated_img.shape

# Calcular el centro de la imagen

cx, cy = int(x // 2), int(y // 2)

# definicion de variables de trasformacion

angulo = 60
theta = math.radians(angulo)
escalamiento = 1/5
traslacion = 10

# aplicando la transformacion

for i in range(x):
    for j in range(y):
        new_x = int((((j - cx) * math.cos(theta) - (i - cy) *
                    math.sin(theta) + cx)*(escalamiento))+traslacion)
        new_y = int((((j - cx) * math.sin(theta) + (i - cy) *
                    math.cos(theta) + cy)*(escalamiento))+traslacion)
        if 0 <= new_x < y and 0 <= new_y < x:
            rotated_img[new_y, new_x] = img[i, j]

# Mostrar la imagen original y la rotada

cv.imshow('Imagen Original', img)
cv.imshow('Imagen Rotada', rotated_img)
cv.waitKey(0)
cv.destroyAllWindows()
