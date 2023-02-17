import cv2 as cv
from datetime import datetime
import numpy as np
import function as func
from matplotlib import pyplot as plt

def resize_templ(templ, percent):
  percent = int(percent)
  width = int(templ.shape[1] * percent / 100)
  height = int(templ.shape[0] * percent / 100)
  resized = cv.resize(templ, (width, height), interpolation=cv.INTER_AREA)
  return resized

def capture_image(path, frame):
  cv.imwrite(path, frame)

cam = cv.VideoCapture(0)
current_timestamp = datetime.timestamp(datetime.now())
captured_path = "captured/{}.png".format(current_timestamp)
dropped_path = "dropped/{}.png".format(current_timestamp)

template = cv.imread('images/temp-card-01.png', 0)
template = resize_templ(template, 30)
w, h = template.shape[1], template.shape[0]

x, y, p_range = func.center_square(cam.get(3), cam.get(4))

while True:
  result, frame = cam.read()
  img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

  res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
  THRESHOLD = 0.7
  loc = np.where(res >= THRESHOLD)
  
  if loc[0].size > 0 :
    # for y, x in zip(loc[0], loc[1]):
    #   cv.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 1)
    # print(loc)
    print('y: ', y, 'x: ', x)
    print('y: ', y+h, 'x: ', x+w)
    capture_image(captured_path, frame)
    print('image saved', captured_path)
    cv.destroyAllWindows()
    break

  # take capture
  if cv.waitKey(13) & 0xFF == ord('q'):
    cv.imshow('CAM', frame)
    cv.imwrite((captured_path), frame)
    cv.destroyAllWindows()
    break
  else :
    frame = cv.rectangle(frame, (x, y), (x + p_range, y + p_range), (255, 0, 0), 1)
    cv.imshow('CAM', frame)

original_image = cv.imread(captured_path)
dropped_image = original_image[y:y+h, x:x+w]
cv.imwrite((dropped_path), dropped_image)
print('dropped image saved', dropped_path)

func.detectcolor(dropped_path)