import cv2 as cv
import numpy as np

# Lee una imagen desde el archivo 'images.jpg'.
img = cv.imread('images.jpg', 1)

# Muestra la imagen original en una ventana llamada 'Original'.
cv.imshow('Original', img)

# 1. Convertir a escala de grises
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Escala de Grises', gray_img)

# 2. Umbralización
_, thresh_img = cv.threshold(gray_img, 128, 255, cv.THRESH_BINARY)
cv.imshow('Umbralización', thresh_img)

# 3. Inversión de colores
inverted_img = cv.bitwise_not(img)
cv.imshow('Inversión de Colores', inverted_img)

# 4. Aumento de brillo
brighter_img = cv.convertScaleAbs(img, alpha=1, beta=50)  # Aumenta el brillo
cv.imshow('Aumento de Brillo', brighter_img)

# 5. Aumento de contraste
contrast_img = cv.convertScaleAbs(img, alpha=2, beta=0)  # Aumenta el contraste
cv.imshow('Aumento de Contraste', contrast_img)

# Espera indefinidamente hasta que el usuario presione una tecla.
cv.waitKey(0)

# Cierra todas las ventanas abiertas por OpenCV.
cv.destroyAllWindows()