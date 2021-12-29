from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
class igm(Screen):
    def change(self):
        self.ids.ikgm.source = "Out_QrCode.png"

class checkifworks(MDApp):
    def build(self):
        manager = ScreenManager()
        manager.add_widget(igm(name="img"))
        return manager

checkifworks().run()


