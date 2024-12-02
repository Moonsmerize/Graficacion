import cv2 as cv
import numpy as np

img = np.ones((500, 500, 3), dtype=np.uint8)*255
# Cielo
cv.rectangle(img, (0,0), (500,300), (228,170,0), -1)
# Sol
cv.circle(img, (400, 80), 40, (0,255,255),-1)
# pasto
cv.rectangle(img, (0,300), (500,500), (0,255,0), -1 )
# Montaña 1
pts = np.array([[0,300],[150,300],[75,150]], np.int32)
pts = pts.reshape((-1,1,2))
cv.fillPoly(img, [pts], (170, 170, 170))
# Montaña 2
pts1 = np.array([[150,300],[300,300],[225,150]], np.int32)
cv.fillPoly(img, [pts1], (170, 170, 170))
# Montaña 3
pts2 = np.array([[300,300],[450,300],[375,150]], np.int32)
cv.fillPoly(img, [pts2], (170, 170, 170))
# Montaña 4
pts3 = np.array([[450,300],[600,300],[525,150]], np.int32)
cv.fillPoly(img, [pts3], (170, 170, 170))
pts5 = np.array([[150,300],[150+37,300-75],[150,150],[150-37,300-75]], np.int32)
cv.fillPoly(img, [pts5], (156, 156, 156))
# Montaña media 1
pts5 = np.array([[0,300],[0+37,300-75],[0,150],[0-37,300-75]], np.int32)
cv.fillPoly(img, [pts5], (156, 156, 156))
# Montaña media 2
pts5 = np.array([[300,300],[300+37,300-75],[300,150],[300-37,300-75]], np.int32)
cv.fillPoly(img, [pts5], (156, 156, 156))
# Montaña media 3
pts5 = np.array([[450,300],[450+37,300-75],[450,150],[450-37,300-75]], np.int32)
cv.fillPoly(img, [pts5], (156, 156, 156))
# Techo Casa
pts4 = np.array([[320,290],[460,290],[390,230]], np.int32)
cv.fillPoly(img, [pts4], (50, 46, 69))
# Casa
cv.rectangle(img, (330,290), (450,400), (59,42,108), -1)
# Puerta
cv.rectangle(img, (360,330), (420,400), (0,0,0), -1)
# Montaña media


cv.imshow('img', img)
cv.waitKey()
cv.destroyAllWindows()