from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout

class cam_class(FloatLayout):
    def start_scan(self, *args):
        for i in self.ids.zbarcam.symbols:
            print(i)



class cam(MDApp):
    def build(self):
        return cam_class

cam().run()