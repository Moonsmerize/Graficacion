import numpy as np
import cv2 as cv
import math

# variables
traslacion_x = 0
traslacion_y = 0

imagen = cv.imread('gas.png')
imagen = cv.resize(imagen, (100, 100))
angulo_rotacion = 0
umbral_movimiento = 30

cap = cv.VideoCapture(0)

lkparm = dict(winSize=(15, 15), maxLevel=2,
              criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

_, vframe = cap.read()
vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)

# Controles
p0 = np.array(
    [(50, 50), (100, 50), (150, 50), (200, 50), (250, 50), (300, 50), (350, 50), (400, 50),(450, 50)])  # Cuatro puntos
p0 = np.float32(p0[:, np.newaxis, :])

mask = np.zeros_like(vframe)

while True:
    _, frame = cap.read()
    frame = cv.flip(frame, 1)
    fgris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    p1, st, err = cv.calcOpticalFlowPyrLK(vgris, fgris, p0, None, **lkparm)

    if p1 is None:
        vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)
        p0 = np.array([(50, 50), (100, 50), (150, 50), (200, 50), (250, 50), (300, 50), (350, 50), (400, 50),(450, 50)])  # Reiniciar los puntos
        p0 = np.float32(p0[:, np.newaxis, :])
        mask = np.zeros_like(vframe)
        cv.imshow('ventana', frame)
    else:
        bp1 = p1[st == 1]
        bp0 = p0[st == 1]

        for i, (nv, vj) in enumerate(zip(bp1, bp0)):
            a, b = (int(x) for x in nv.ravel())
            c, d = (int(x) for x in vj.ravel())
            dist = np.linalg.norm(nv.ravel() - vj.ravel())

            frame = cv.line(frame, (c, d), (a, b), (0, 0, 255), 2)
            frame = cv.circle(frame, (c, d), 2, (255, 0, 0), -1)
            frame = cv.circle(frame, (a, b), 3, (0, 255, 0), -1)

            # primer punto
            if i == 0 and dist > umbral_movimiento:  # Solo para el primer punto
                angulo_rotacion += 10  # Aumentar el ángulo de rotación
            # segundo punto
            if i == 1 and dist > umbral_movimiento:
                angulo_rotacion -= 10  # Aumentar el ángulo de rotación
            # tercer punto
            if i == 2 and dist > umbral_movimiento:
                imagen = cv.resize(imagen, None, fx=0.9, fy=0.9)
            # cuarto punto
            if i == 3 and dist > umbral_movimiento:
                imagen = cv.resize(imagen, None, fx=1.1, fy=1.1)
            # quinto punto
            if i == 4 and dist > umbral_movimiento:
                traslacion_x += 5
            # sexto punto
            if i == 5 and dist > umbral_movimiento:
                traslacion_x -= 5
            # septimo punto
            if i == 6 and dist > umbral_movimiento:
                traslacion_y += 5
            # octavo punto
            if i == 7 and dist > umbral_movimiento:
                traslacion_y -= 5

        # posicion de la imagen
        h, w, _ = imagen.shape
        center_x = frame.shape[1] // 2 - w // 2 + traslacion_x
        center_y = frame.shape[0] // 2 - h // 2 + traslacion_y

        # Rotar la imagen
        M = cv.getRotationMatrix2D((w // 2, h // 2), angulo_rotacion, 1.0)
        imagen_rotada = cv.warpAffine(imagen, M, (w, h))

        # Superponer la imagen rotada en el marco
        frame[center_y:center_y + h, center_x:center_x + w] = imagen_rotada
        cv.imshow('ventana', frame)
        vgris = fgris.copy()

        if (cv.waitKey(1) & 0xff) == 27:
            break

cap.release()
cv.destroyAllWindows()
