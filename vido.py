# coding:utf-8
import sys
from datetime import datetime

from kivy.app import App
import ast
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from kivymd.app import MDApp
qrCodeDetector = cv2.QRCodeDetector()

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)
        Clock.schedule_interval(self.check, 2.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
    def check(self, *args):
        ret, frame = self.capture.read()
        decodedText, points, _ = qrCodeDetector.detectAndDecode(frame)

        for i in decodedText:

            decodedText2 = ast.literal_eval(decodedText)
            print(decodedText2)

            print(type(decodedText2))
            if decodedText2[0] == "Sanjay":
                sys.exit()

            x = datetime.now()

            print(x.year, x.day, x.month, x.hour, x.minute)


class CamApp(MDApp):
    def build(self):
        self.capture = cv2.VideoCapture(1)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()