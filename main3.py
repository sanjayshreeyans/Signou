from datetime import datetime

from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout


class form (FloatLayout):
  def take_values(self):
      name = str(self.ids.namebox.text)
      email = str(self.ids.emailbox.text)
      grade = str(self.ids.gradebox.text)
      teacher = str(self.ids.teacherbox.text)
      x = datetime.now()

      print(x.year, x.day, x.month, x.hour, x.minute)
      print(name, email, grade, teacher)

class prototypeform(MDApp):
  def build(self):
    self.theme_cls.primary_palette = "Purple"
    self.title = "Signout Form"

    return form()
prototypeform().run()