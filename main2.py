import ast
import json
from kivy.core.window import Window
from kivy.uix.image import Image
from functools import partial
from datetime import datetime
import imutils
import cv2
import pyrebase
import random
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
import qrcode
import os

ds = os.path.split(os.getcwd())
path = ds[0] + "/" + ds[1]  # alwats append
print(path, "PATTTTTTTHHHHH")

# Window.size = (400, 750)

s = []
name_of_the_current_user = ""
new_user = False
firebaseConfig = {
    "apiKey": "AIzaSyDXRu2omq3p2KBfoj-0wj0iQ2kKnT60Jp8",
    "authDomain": "restroomsignout-bbcaf.firebaseapp.com",
    "projectId": "restroomsignout-bbcaf",
    "databaseURL": "https://restroomsignout-bbcaf-default-rtdb.firebaseio.com/",
    "storageBucket": "restroomsignout-bbcaf.appspot.com",
    "messagingSenderId": "120464602127",
    "appId": "1:120464602127:web:721a35455fd0c431fbdf7a",
    "measurementId": "G-JTHT4M7KE0"
}

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
auth = firebase.auth()


class CreateAAccountScreen(Screen):
    def on_enter(self, *args):
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
                "height": 1,

            }
        ]
        self.dropdown = MDDropdownMenu(caller=caller, items=menu_items, width_mult=4, position='bottom',
                                       callback=self.menu_callback, max_height=dp(120), border_margin=dp(250),
                                       ver_growth="down")
        self.dropdown.bind()

    def menu_callback(self, instance_menu):
        print(instance_menu.text)
        self.ids.caller.text = str(instance_menu.text)
        self.dropdown.dismiss()

    def drop(self):
        self.dropdown.open()

    def createanewaccount(self):
        email = str(self.ids.emailboxsignup.text)
        password = str(self.ids.passwordboxsignup.text)
        name = str(self.ids.username.text)
        grade = str(self.ids.caller.text)
        auth.create_user_with_email_and_password(email, password)
        login_info = {"email": email, "Password": password, "name": name, "Grade": grade, "New_User": True}
        print(login_info, "PRE")
        database.child(str(grade)).child(str(name)).child("Login Info").set(login_info)
        database.child("Users_Login").child(str(name)).set(login_info)
        globals()['new_user'] = True


name_of_the_current_user = ""
grade_of_the_current_user = ''
is_the_current_user_a_teacher = ''
email_of_the_current_user = ""


class Create_an_account_with_access_code(Screen):
    def Create_a_teacher_account(self):
        teacher_email = self.ids.teacheremail.text
        teacher_password = self.ids.teacherpass.text
        teacher_name = self.ids.teachername.text
        teacher_account_code = self.ids.access_code.text
        if teacher_account_code == "H89l":
            auth.create_user_with_email_and_password(teacher_email, teacher_password)
            login_info = {"email": teacher_email, "Password": teacher_password, "name": teacher_name,
                          "Grade": "TEACHER"}
            print(login_info, "PRE")
            # database.child("Teacher").child(str(teacher_name)).child("Login Info").set(login_info)
            database.child("Users_Login").child(str(teacher_name)).set(login_info)


class LoginScreenExistingUsers(Screen):

    def on_enter(self, *args):

        Clock.schedule_once(self.set_toolbar_font_size)

    def set_toolbar_font_size(self, *args):
        self.ids.toolbar.ids.label_title.font_size = '25sp'
        # Remove in Deployment
        self.ids.emailbox.text = "presentation_demo@gmail.com"
        self.ids.passwordbox.text = "Sanjay@123"
        # Remove in Deployment

    def logintofirebase(self, email="", password=""):

        email = str(self.ids.emailbox.text)
        password = str(self.ids.passwordbox.text)
        try:
            auth.sign_in_with_email_and_password(email, password)
            print(email, password)

            self.ids.labelforinfo.text = "Sucessful in " + str(email)
            self.ids.labelforinfo.color = (0, 0.8, 0, 1)
            self.ids.labelforinfo.pos_hint = {"center_x": 0.95, "center_y": 0.2}

            # MDApp.get_running_app().root.current = ""
            for i in database.child("Users_Login").get().each():
                if email == i.val().get("email"):
                    globals()['email_of_the_current_user'] = str(i.val().get("email"))
                    globals()['name_of_the_current_user'] = str(i.val().get("name"))
                    if str(i.val().get("Grade")) == "TEACHER":
                        print("The current user is a Teacher")
                        globals()['is_the_current_user_a_teacher'] = True
                        globals()['grade_of_the_current_user'] = "None"
                    else:
                        print("The current user is not a Teacher")
                        globals()['is_the_current_user_a_teacher'] = False
                        globals()['grade_of_the_current_user'] = str(i.val().get("Grade"))
                    print(globals()['name_of_the_current_user'], globals()['name_of_the_current_user'], "SS")
            MDApp.get_running_app().root.current = "Home_Screen"



        except Exception as d:
            ds = str(json.loads(d.args[1])['error']['message'])
            print(ds)
            s = ds.replace("_", " ")
            print(s, "AFTER")

            self.ids.labelforinfo.text = str(s)

            self.ids.labelforinfo.color = (1, 0, 0, 1)
            self.ids.labelforinfo.pos_hint = {"center_x": 0.84, "center_y": 0.2}

            print(d)


class Home_Screen(Screen):
    def on_enter(self, *args):
        if globals()['is_the_current_user_a_teacher']:
            pass
        else:
            if globals()['new_user']:
                pass

            new_user = database.child(str(globals()['grade_of_the_current_user'])).child(
                str(globals()['name_of_the_current_user'])).child("Login Info").get().val()
            if new_user['New_User']:
                pass
            else:
                gh = database.child(str(globals()['grade_of_the_current_user'])).child(
                    str(globals()['name_of_the_current_user'])).child("Signouts").child("Latest_Val").get().val()

                if gh['Completed full Cycle']:
                    print("Looks Like everything is good. Proceeding to the QR code Scanner")
                else:
                    print("Oops a Request isn't closed, Rerouting to the Accepted Page")

                    path = str((globals()['grade_of_the_current_user']) + "," + str(globals()['name_of_the_current_user']) + ",""Signouts" + "," +gh['Time Left'])

                    info_lst = path
                    # [name, grade, teacher_name, unique_id,email]

                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=20,
                        border=4,
                    )
                    qr.add_data(info_lst)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    path_img = globals()['path'] + "/Out_QrCode.png"
                    img.save(path_img)
                    dgp = Accepted_page()
                    dgp.call(gh['Time Left'])
                    MDApp.get_running_app().root.current = "Accepted_page"

    def switch_to_dectect_page(self):

        if globals()['is_the_current_user_a_teacher']:
            MDApp.get_running_app().root.current = "dectectpage_teacher"
            print(globals()['is_the_current_user_a_teacher'])
        else:
            print(globals()['is_the_current_user_a_teacher'])

            MDApp.get_running_app().root.current = "dectectpage"


class KivyCamera(Screen, Image):
    def on_enter(self, *args):
        self.qrCodeDetector = cv2.QRCodeDetector()
        self.capture = cv2.VideoCapture(1)
        self.my_camera = self.capture
        self.fps = 30

        self.d = Clock.schedule_interval(self.update, 1.0 / self.fps)
        self.e = Clock.schedule_interval(self.check, 2.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        print("UPDATE_Student")
        frame = imutils.resize(frame, width=Window.size[0], height=Window.size[1])
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()

            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.ids.img.texture = image_texture

    def check(self, *args):
        allowed = True
        ret, frame = self.capture.read()
        decodedText, points, _ = self.qrCodeDetector.detectAndDecode(frame)

        for i in decodedText:

            decodedText2 = ast.literal_eval(decodedText)
            print(decodedText2)

            print(type(decodedText2), "Student")
            if decodedText2[0] == "Sanjay":
                if allowed:
                    print(decodedText2, "DECODED")
                    f = Accepted_page()
                    f.send_info(decodedText2)
                    MDApp.get_running_app().root.current = "Accepted_page"

                    self.d.cancel()
                    self.e.cancel()
                    self.capture.release()
                    allowed = False


class KivyCamera_Teacher(Screen, Image):
    def on_enter(self, *args):
        self.qrCodeDetector = cv2.QRCodeDetector()
        self.capture = cv2.VideoCapture(1)
        self.my_camera = self.capture
        self.fps = 30

        self.d = Clock.schedule_interval(self.update, 1.0 / self.fps)
        self.e = Clock.schedule_interval(self.check, 2.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        print("UPDATE_Teacher")
        frame = imutils.resize(frame, width=Window.size[0], height=Window.size[1])
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()

            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.ids.img.texture = image_texture

    def check(self, *args):
        allowed = True
        ret, frame = self.capture.read()
        decodedText, points, _ = self.qrCodeDetector.detectAndDecode(frame)
        # Write Rules for scaning, Sanjay has alredy implemented email.
        for i in decodedText:





            print(decodedText, "After string manipulation")
            decodedText2 = decodedText.split(",")
            print(decodedText2)

            print(type(decodedText2), "Teacher")
            print(len(decodedText2), "Teacher")
            if len(decodedText2) == 4:
                if allowed:
                    print(decodedText2, "DECODED_Teacher")
                    allowed = False
                    self.d.cancel()
                    self.e.cancel()
                    self.capture.release()
                    f = Accepted_page_Teacher()
                    f.send_info(decodedText2)
                    MDApp.get_running_app().root.current = "Accepted_page_Teacher"


class Accepted_page_Teacher(Screen, Image):
    # def call(self):
    #     Clock.schedule_interval(self.refresh, 1.0)
    #     # self.df = Image(source="/Users/sanjayshreeyansgmail.com/PycharmProjects/SignoutApp/Out_QrCode.png")
    #
    # def refresh(self, *args):
    #     print("REFRESH")
    #     f = str("/Users/sanjayshreeyansgmail.com/PycharmProjects/SignoutApp/Out_QrCode.png")
    #
    #     self.ids.ikgm.source = f
    #
    #     self.ids.ikgm.reload()
    #     print(self.ids.ikgm.source)
    def switchscreen(self):
        MDApp.get_running_app().root.current = "Home_Screen"

    def send_info(self, lst):
        print(lst, "Send Info")
        grade = lst[0]
        name = lst[1]
        which_folder = lst[2]
        time_specified = lst[3]
        x = datetime.now()
        self.time = str(x.month) + "/" + str(x.day) + "/" + str(str(x.year) + " " + str(x.hour) + ":" + str(x.minute))
        print(self.time, "Time, Send Info")
        print(type(self.time))
        d = database.child(grade).child(name).child(which_folder).child(time_specified).get().val()
        print(d['Completed full Cycle'], "JJJJJJJJJJJJJJJJJJJJJJJ")
        d['Completed full Cycle'] = True
        d['Time Returned'] = self.time
        database.child(grade).child(name).child(which_folder).child(time_specified).set(d)

        gh = database.child(grade).child(name).child("Signouts").child("Latest_Val").get().val()
        gh['Completed full Cycle'] = True
        gh['Time Returned'] = self.time
        database.child(grade).child(name).child("Signouts").child("Latest_Val").set(gh)

        print("D")

    #
    # def create_qr_code(self, lst_info, id):
    #     print("Insdie creation")
    #     name = str(globals()['name_of_the_current_user']),
    #     grade = str(globals()['grade_of_the_current_user'])
    #     email = str(globals()['email_of_the_current_user'])
    #     teacher_name = lst_info[0]
    #     unique_id = id
    #     info_lst = [name, grade, teacher_name, unique_id,email]
    #
    #     qr = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=10,
    #         border=4,
    #     )
    #     qr.add_data(info_lst)
    #     qr.make(fit=True)
    #
    #     img = qr.make_image(fill_color="black", back_color="white")
    #
    #     img.save("Out_QrCode.png")
    #     f = str("Out_QrCode.png")
    #
    #     self.ids.ikgm.source = "great.png"
    #     self.ids.ikgm.reload()
    #


class Accepted_page(Screen, Image):
    def call(self, time):

        self.hj = Clock.schedule_interval(partial(self.refresh, time=time), 3.0)
        # self.df = Image(source="/Users/sanjayshreeyansgmail.com/PycharmProjects/SignoutApp/Out_QrCode.png")

    def refresh(self, *args, time):
        f = database.child(str(globals()['grade_of_the_current_user'])).child(
            str(globals()['name_of_the_current_user'])).child("Signouts").child(str(time)).get().val()
        print("Checking", f)
        if f['Completed full Cycle']:
            self.hj.cancel()

            MDApp.get_running_app().root.current = "Verified_Screen_Student"


        else:
            print("No complete")

    def send_info(self, lst):
        print(lst, "Send Info")
        email = str(globals()['email_of_the_current_user'])
        x = datetime.now()
        self.time = str(x.month) + "/" + str(x.day) + "/" + str(str(x.year) + " " + str(x.hour) + ":" + str(x.minute))
        print(self.time, "Time, Send Info")
        print(type(self.time))
        unique_id = int(random.randint(1, 10000))

        info_dict = {"Student Name": str(globals()['name_of_the_current_user']), "Teacher Name": lst[0],
                     "Room No: ": lst[1], "Time Left": self.time, "ID": unique_id,
                     "Email": str(globals()['email_of_the_current_user']), "Completed full Cycle": False}
        print(info_dict, "Dict, Send info")
        database.child(str(globals()['grade_of_the_current_user'])).child(
            str(globals()['name_of_the_current_user'])).child("Signouts").child(str(self.time)).set(info_dict)

        database.child(str(globals()['grade_of_the_current_user'])).child(
            str(globals()['name_of_the_current_user'])).child("Signouts").child("Latest_Val").set(info_dict)
        print("Info Sent")

        self.create_qr_code(lst, unique_id, self.time)

    def create_qr_code(self, lst_info, id, time):
        print("Insdie creation")
        name = str(globals()['name_of_the_current_user']),
        grade = str(globals()['grade_of_the_current_user'])
        email = str(globals()['email_of_the_current_user'])
        path = str(str(globals()['grade_of_the_current_user']) + "," + str(globals()['name_of_the_current_user']) + "," + "Signouts" + ","+
                time)
        teacher_name = lst_info[0]
        unique_id = id
        info_lst = path
        # [name, grade, teacher_name, unique_id,email]

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr.add_data(info_lst)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        path_img = globals()['path'] + "/Out_QrCode.png"
        img.save(path_img)

        self.call(time)


class Verified_Screen_Student(Screen):
    def switchscreen(self):
        MDApp.get_running_app().root.current = "Home_Screen"


class main(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.title = "Signout"
        manager = ScreenManager()  # Initializing Screen Manager
        manager.add_widget(LoginScreenExistingUsers(name="LoginScreenExistingUsers"))

        manager.add_widget(Home_Screen(name="Home_Screen"))

        manager.add_widget(CreateAAccountScreen(name="CreateAAccountScreen"))

        manager.add_widget(KivyCamera(name="dectectpage"))

        manager.add_widget(KivyCamera_Teacher(name="dectectpage_teacher"))

        manager.add_widget(Accepted_page(name="Accepted_page"))

        manager.add_widget(Verified_Screen_Student(name="Verified_Screen_Student"))

        manager.add_widget(Accepted_page_Teacher(name="Accepted_page_Teacher"))

        manager.add_widget(Create_an_account_with_access_code(name="Create_an_account_with_access_code"))

        return manager


main().run()
