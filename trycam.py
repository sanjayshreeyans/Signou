'''
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a buttoned labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.

'''
'''
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a buttoned labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.

'''

# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time
import zbarlight
Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    #:import ZBarCam kivy_garden.zbarcam.ZBarCam
    ZBarCam:
        id: qrcodecam
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
    
''')

class CameraClick(BoxLayout):
    def capture(self):
        cam = self.ids.camera.texture

        codes = zbarlight.scan_codes(['qrcode'], cam)
        print(codes)

        print("Captured")


class TestCamera(App):

    def build(self):
        return CameraClick()

TestCamera().run()