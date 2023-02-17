import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('captured/cac.png')
crop = img[203:563, 395:755]
plt.imshow(crop)
plt.show()