import cv2 as cv
from datetime import datetime
import numpy as np
import function as func

def resize_templ(templ, percent):
  percent = int(percent)
  width = int(templ.shape[1] * percent / 100)
  height = int(templ.shape[0] * percent / 100)
  resized = cv.resize(templ, (width, height), interpolation=cv.INTER_AREA)
  return resized

cam = cv.VideoCapture(0)
captured_path = "captured/{}.png".format(datetime.timestamp(datetime.now()))
template = cv.imread('images/template3.png', 0)
# template = resize_templ(template, 30)
w, h = template.shape[1], template.shape[0]

x, y, p_range = func.center_square(cam.get(3), cam.get(4))

while True:
  result, frame = cam.read()
  img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

  res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
  THRESHOLD = 0.8
  loc = np.where(res >= THRESHOLD)
  
  if loc[0].size > 0 :
    for y, x in zip(loc[0], loc[1]):
      cv.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 1)
    print(loc)

  # take capture
  if cv.waitKey(13) & 0xFF == ord('q'):
    cv.imshow('CAM', frame)
    cv.imwrite((captured_path), frame)
    cv.destroyAllWindows()
    break
  else :
    # frame = cv.rectangle(frame, (x, y), (x + p_range, y + p_range), (255, 0, 0), 1)
    cv.imshow('CAM', frame)
