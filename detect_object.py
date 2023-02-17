import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

def resize_templ(templ, percent):
  percent = int(percent)
  width = int(templ.shape[1] * percent / 100)
  height = int(templ.shape[0] * percent / 100)
  resized = cv.resize(templ, (width, height), interpolation=cv.INTER_AREA)
  return resized

img_rgb = cv.imread('images/image2.jpg')
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
templ = cv.imread('images/template3.jpg', 0)

template = resize_templ(templ, 50)

height = template.shape[0]
width = template.shape[1]

res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF)

plt.imshow(res, cmap='gray')
# plt.show()
threshold = 0.9 #For TM_CCOEFF_NORMED, larger values = good fit.

loc = np.where( res >= threshold)  
for y, x in zip(loc[0], loc[1]): 
    cv.rectangle(img_rgb, (x, y), (x + width, y + height), (255, 0, 0), 1) 

cv.imshow("Matched image", img_rgb)
cv.waitKey()
cv.destroyAllWindows()