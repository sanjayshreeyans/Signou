import qrcode
import ast
import time

# from PIL import Image
# lsit = "Sanjay", 123
# img = qrcode.make(list(lsit))
# img.save("FFF.png")
import zbar

scanner = zbar.Scanner()

import cv2
cap = cv2.VideoCapture(1)
cap.set(3,680)
cap.set(4,480)
qrCodeDetector = cv2.QRCodeDetector()

import datetime
import numpy
from PIL import Image

while True:

    success, img  = cap.read()
    decodedText, points, _ = qrCodeDetector.detectAndDecode(img)
    if decodedText == "":
        print("Hi",decodedText)
    else:
        for i in decodedText:

            print(decodedText)
            print(type(decodedText))


            x = datetime.datetime.now()

            print(x.year, x.day, x.month,x.hour, x.minute)

    cv2.imshow("Result:", img)
    cv2.waitKey(0)

 #  cv2.
# val_list = ast.literal_eval(val)

