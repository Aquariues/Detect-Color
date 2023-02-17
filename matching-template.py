import cv2  
import matplotlib.pyplot as plt
import numpy as np

def imshow(img, figsize=(6, 6)):
    fig, ax = plt.subplots(1, 1, figsize=(figsize))
    ax.axis('off')
    ax.imshow(img)
    plt.show()
    
img = cv2.imread('images/image1.jpg')
#Convert to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.imread('images/template2.jpg', 0)
w, h = template.shape[1], template.shape[0]

res = cv2.matchTemplate(img_gray,template, cv2.TM_CCOEFF_NORMED)
imshow(res)

THRESHOLD = 0.9
loc = np.where(res >= THRESHOLD)
print(loc)
#Draw boudning box
for y, x in zip(loc[0], loc[1]):
    cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,0), 1)
imshow(img)