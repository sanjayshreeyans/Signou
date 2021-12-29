import qrcode
import ast
import time
from kivy.clock import Clock

# from PIL import Image
# lsit = "Sanjay", 123
# img = qrcode.make(list(lsit))
# img.save("FFF.png")

import cv2
cap = cv2.VideoCapture(1)
cap.set(3,680)
cap.set(4,480)
qrCodeDetector = cv2.QRCodeDetector()

import datetime
import numpy
from PIL import Image

def dectect(*args):
    while True:

        success, img = cap.read()
        cv2.imshow("Result:", img)

        decodedText, points, _ = qrCodeDetector.detectAndDecode(img)


        for i in decodedText:
            print(decodedText)
            print(type(decodedText))

            x = datetime.datetime.now()

            print(x.year, x.day, x.month, x.hour, x.minute)
        cv2.imshow("Result:", img)
        cv2.waitKey(1)

dectect()

# Clock.schedule_interval(dectect, 1.0/30.0)
# def wow():
#     print("Woow")
#

# from event_scheduler import EventScheduler
#
# event_scheduler = EventScheduler()
# event_scheduler.start()
# #Schedule the recurring event to print "hello world" every 60 seconds with priority 1
# #You can use the event_id to cancel the recurring event later
# event_id = event_scheduler.enter_recurring(1/60,1, dectect)

