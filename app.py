import cv2
import numpy as np
from twilio.rest import TwilioRestClient
from skimage.measure import compare_ssim

ACCOUNT_SID = 'ACCOUNT_SID'
AUTH_TOKEN = 'AUTH_TOKEN'
TWILIO_PHONE = 'TWILIO_PHONE'
RECEIVER_PHONE = 'RECEIVER_PHONE'

def ssim(A,B):
  return compare_ssim(A,B, data_range=A.max()-A.min())

def mse(A,B):
  return ((A-B)**2).mean()

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

# Video Input
cap = cv2.VideoCapture('Shooting_Form.mp4')

# Camera Input
# cap = cv2.VideoCapture(0)

curr_frame = None
prev_frame = None
first_frame = True
frame_counter = 0
first_msg = True

while True:
  if frame_counter == 0:
    prev_frame = curr_frame
  _, curr_frame = cap.read()
  if curr_frame is None:
    break

  curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
  if first_frame:
    prev_frame = curr_frame
    first_frame = False

  if frame_counter == 9:
    # print(mse(curr_frame, prev_frame))
    ssim_index = ssim(curr_frame, prev_frame)
    if ssim_index < 0.8 and first_msg:
      client.messages.create(to=RECEIVER_PHONE, from_=TWILIO_PHONE, body="Intruder Alert!")
      first_msg = False
    frame_counter = 0

  cv2.imshow('app', curr_frame)
  frame_counter = frame_counter + 1

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()