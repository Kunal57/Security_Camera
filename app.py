import cv2
import numpy as np

# Video Input
cap = cv2.VideoCapture('Shooting_Form.mp4')

# Camera Input
# cap = cv2.VideoCapture(0)

while True:
  _, frame = cap.read()
  if frame is None:
    break
  cv2.imshow('app', frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()