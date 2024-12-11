import cv2 as cv
import numpy as np

img = np.ones((500, 500), dtype=np.uint8)*255

for i in range(50):
    cv.circle(img, (250, 250), 20+i, (0, 234, 21), -1)
    cv.imshow('img', img)
    img = np.ones((500, 500, 3), dtype=np.uint8)*255
    cv.waitKey(40)


cv.waitKey(0)
cv.destroyAllWindows()
