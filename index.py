import cv2 as cv
from datetime import datetime
import function as func

cam = cv.VideoCapture(0)
captured_path = "captured/{}.png".format(datetime.timestamp(datetime.now()))

x, y, p_range = func.center_square(cam.get(3), cam.get(4))

while True:
  result, frame = cam.read()
  
  # take capture
  if cv.waitKey(13) & 0xFF == ord('\r'):
    cv.imshow('CAM', frame)
    cv.imwrite((captured_path), frame)
    cv.destroyAllWindows()
    break
  else :
    frame = cv.rectangle(frame, (x, y), (x + p_range, y + p_range), (255, 0, 0), 1)
    cv.imshow('CAM',frame)

func.detectcolor(url = captured_path, cvt_color = cv.COLOR_BGR2HLS)