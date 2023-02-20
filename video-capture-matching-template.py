import cv2 as cv
from datetime import datetime
import numpy as np
import detectColor as func
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
template = resize_templ(template, 25)
w, h = template.shape[1], template.shape[0]

x, y, p_range = func.center_square(cam.get(3), cam.get(4))
# RGB - 158, 48, 48 -  19, 138, 99 - 45, 45, 145
x_cam_range = x + p_range + 5
y_cam_range = y + p_range + 5
drop_value_y, drop_value_y_plus = 0, 0
drop_value_x, drop_value_x_plus = 0, 0
while True:
  result, frame = cam.read()
  img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

  res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
  THRESHOLD = 0.65
  loc = np.where(res >= THRESHOLD)
  
  if loc[0].size > 0 :
    for y1, x1 in zip(loc[0], loc[1]):
      print(y, y_cam_range, x, x_cam_range)
      print(y1, y1+h, x1, x1+w)
      drop_value_y, drop_value_y_plus = y1, y1+h
      drop_value_x, drop_value_x_plus = x1, x1+w
    # auto capture when detected object
    capture_image(captured_path, frame)
    print('image saved', captured_path)
    cv.destroyAllWindows()
    break

  # take capture
  if cv.waitKey(13) & 0xFF == ord('q'):
    cv.destroyAllWindows()
    break
  else :
    # frame = cv.rectangle(frame, (x, y), (x_cam_range, y_cam_range), (255, 0, 0), 1)
    cv.imshow('CAM', frame)

# drop captured image 
original_image = cv.imread(captured_path)
dropped_image = original_image[drop_value_y:drop_value_y_plus, drop_value_x: drop_value_x_plus]
cv.imwrite((dropped_path), dropped_image)
print('dropped image saved', dropped_path)

# detect dropped image
func.detectcolor(dropped_path, cv.COLOR_BGR2HSV)