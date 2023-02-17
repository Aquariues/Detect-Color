import function as func
import cv2 as cv

cam = cv.VideoCapture(0)
detectQR = cv.QRCodeDetector()
x, y, p_range = func.center_square(cam.get(3), cam.get(4))
temp = cv.imread('images/qr.png')

data, bbox, _ = detectQR.detectAndDecode(temp)

while True:
  result, frame = cam.read()
  data, bbox, _ = detectQR.detectAndDecode(frame)
  
  if data:
    print(data)
  # take capture
  if cv.waitKey(13) & 0xFF == ord('q'):
    cv.imshow('CAM', frame)
    cv.destroyAllWindows()
    break
  else :
    frame = cv.rectangle(frame, (x, y), (x + p_range, y + p_range), (255, 0, 0), 1)
    cv.imshow('CAM',frame)
