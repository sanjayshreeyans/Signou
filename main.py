import json

import pyrebase
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

s = []
name_of_the_current_user = ""
firebaseConfig = {
  "apiKey": "AIzaSyDXRu2omq3p2KBfoj-0wj0iQ2kKnT60Jp8",
  "authDomain": "restroomsignout-bbcaf.firebaseapp.com",
  "projectId": "restroomsignout-bbcaf",
  "databaseURL": "https://console.firebase.google.com/project/restroomsignout-bbcaf/database/restroomsignout-bbcaf-default-rtdb/data",
  "storageBucket": "restroomsignout-bbcaf.appspot.com",
  "messagingSenderId": "120464602127",
  "appId": "1:120464602127:web:721a35455fd0c431fbdf7a",
  "measurementId": "G-JTHT4M7KE0"
}


firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
auth = firebase.auth()


class CreateAAccountScreen(Screen):
  def on_kv_post(self, base_widget):
    caller = self.ids.caller
    menu_items = [
      {
        "viewclass": "OneLineListItem",

        "text": f"7th Grade",
        "height": 1,

      },

      {
        "viewclass": "OneLineListItem",

        "text": f"8th Grade",
        "height":1,

      }
    ]
    self.dropdown = MDDropdownMenu(caller=caller, items=menu_items, width_mult=4,position='bottom',callback=self.menu_callback,max_height=dp(120),border_margin=dp(250),ver_growth="down")
    self.dropdown.bind()

  def menu_callback(self, instance_menu):
    print(instance_menu.text)
    self.ids.caller.text =str(instance_menu.text)
    self.dropdown.dismiss()
  def drop(self):
    self.dropdown.open()
  def createanewaccount(self):
    email = str(self.ids.emailboxsignup.text)
    password = str(self.ids.passwordboxsignup.text)
    name = str(self.ids.username)
    auth.create_user_with_email_and_password(email, password)
    login_info = {"Email": email, "Password":password,  "Usename": name}
    database.child("Users").child(name).child("Login Info").put(login_info)



class LoginScreenExistingUsers(Screen):

  def on_enter(self, *args):

    Clock.schedule_once(self.set_toolbar_font_size)

  def set_toolbar_font_size(self, *args):
    self.ids.toolbar.ids.label_title.font_size = '25sp'

  def logintofirebase(self, email="", password=""):

      email = str(self.ids.emailbox.text)
      password = str(self.ids.passwordbox.text)
      try:
        auth.sign_in_with_email_and_password(email, password)
        print(email, password)

        self.ids.labelforinfo.text = "Sucessful in " + str(email)
        self.ids.labelforinfo.color = (0, 0.8, 0, 1)
        self.ids.labelforinfo.pos_hint = {"center_x": 0.95, "center_y": 0.2}

        #MDApp.get_running_app().root.current = "homescreenclass"



      except Exception as d:
        ds = str(json.loads(d.args[1])['error']['message'])
        print(ds)
        s = ds.replace("_", " ")
        print(s, "AFTER")

        self.ids.labelforinfo.text = str(s)

        self.ids.labelforinfo.color = (1, 0, 0, 1)
        self.ids.labelforinfo.pos_hint = {"center_x": 0.84, "center_y": 0.2}

        print(d)


class Signout(MDApp):
  def build(self):

    self.theme_cls.primary_palette = "Purple"
    self.title = "Signout"
    manager = ScreenManager()  # Initializing Screen Manager
    manager.add_widget(LoginScreenExistingUsers(name="LoginScreenExistingUsers"))
    manager.add_widget(CreateAAccountScreen(name="CreateAAccountScreen"))
    return manager
Signout().run()