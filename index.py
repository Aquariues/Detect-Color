import cv2 as cv
from datetime import datetime
import numpy as np
import detectColor as func
import time

cam = cv.VideoCapture(0)

print('cam w - h: ', cam.get(3), cam.get(4))

current_timestamp = datetime.timestamp(datetime.now())
captured_path = "captured/{}.png".format(current_timestamp)
dropped_path = "dropped/{}.png".format(current_timestamp)

template = cv.imread('images/temp-card-01.png', 0)
print('template: ', template.shape[0], template.shape[1])

x, y, p_range = func.center_square(cam.get(3), cam.get(4))
print('square y - x - p_range: ', y, x, p_range)

template = func.resize_templ(template, p_range)
w, h = template.shape[1], template.shape[0]
print('template resized: ', h, w)

x_cam_range = x + p_range + 5
y_cam_range = y + p_range + 5
drop_value_y, drop_value_y_plus = 0, 0
drop_value_x, drop_value_x_plus = 0, 0

while True:
  result, frame = cam.read()
  img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
  THRESHOLD = 0.6
  res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
  loc = np.where(res >= THRESHOLD)
  
  if loc[0].size > 0 :
    print('Colour Card Detected !')
    for y1, x1 in zip(loc[0], loc[1]):
      print(y, y_cam_range, x, x_cam_range)
      print(y1, y1 + p_range, x1, x1 + p_range)
      drop_value_y, drop_value_y_plus = y1, y1 + p_range
      drop_value_x, drop_value_x_plus = x1, x1 + p_range
    # auto capture when detected object
    func.capture_image(captured_path, frame)
    print('Image captured: ', captured_path)
    print('Close after 2 seconds...')
    time.sleep(2)
    cv.destroyAllWindows()
    break

  # take capture
  if cv.waitKey(13) & 0xFF == ord('q'):
    cv.destroyAllWindows()
    break
  else :
    frame = cv.rectangle(frame, (x, y), (x_cam_range, y_cam_range), (255, 0, 0), 1)
    cv.imshow('CAM', frame)

# drop captured image 
original_image = cv.imread(captured_path)
dropped_image = original_image[drop_value_y:drop_value_y_plus, drop_value_x: drop_value_x_plus]
cv.imwrite((dropped_path), dropped_image)
print('Drop the colour card from image: ', dropped_path)

# detect dropped image
func.detectcolor(dropped_path, cv.COLOR_BGR2HSV)