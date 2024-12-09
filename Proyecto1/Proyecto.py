import cv2
import numpy as np

imagen = 'triangulo1.png'
mask = cv2.imread('triangulo.png', cv2.IMREAD_UNCHANGED)  # Cargar la máscara

imagen = cv2.imread(imagen, cv2.IMREAD_UNCHANGED)
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        break

    height, width, channels = frame.shape
    mask_height, mask_width, mask_channels = mask.shape

    # Calcular la posición de la máscara en el centro
    x_offset = (width - mask_width) // 2
    y_offset = (height - mask_height) // 2

    # Combinar la máscara con el frame
    alpha = 0.5
    beta = 1.0 - alpha
    frame[y_offset:y_offset+mask_height, x_offset:x_offset+mask_width] = \
        cv2.addWeighted(frame[y_offset:y_offset+mask_height, x_offset:x_offset+mask_width], beta,
                        mask, alpha, 0.0)

    cv2.imshow('Video con mascara', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()