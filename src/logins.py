import kivy
from kivy.animation import Animation
import sqlite3
import datetime
from kivymd.uix.behaviors import HoverBehavior
from matplotlib.widgets import Button

import src.exceptions as exceptions
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDRoundFlatButton

class Logo(Screen):
    pass

class AnimatedButtons(Button, HoverBehavior):

    def on_enter(self):
        self.background = (251/255, 104/255, 23/255, 1)
        # Animation().start(self, MDRoundFlatButton)

    def on_leave(self):
        self.background = (71/255, 104/255, 237/255, 1)

    # def animate_it(self,MDRoundFlatButton, *args):
    #     animate = Animation(d=3, size=self.size_hint_x = 1)
    #     animate.start(MDRoundFlatButton)


class Authorization(Screen):
    pass


class LogIn(Screen):
    def log_in(self):
        self.date = datetime.datetime.today()
        try:
            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE users_account
                        SET
                        entered_password = ?
                        WHERE
                        users_account.staff_id =?
                         """, (self.ids.password.text, self.ids.staff_id.text,))
            conn.commit()

            password = [r[0] for r in c.execute(
                """SELECT password FROM users_account
                            WHERE staff_id = ?""", (self.ids.staff_id.text,))]
            entered_password = [r[0] for r in c.execute(
                """SELECT entered_password FROM users_account
                            WHERE staff_id = ?""", (self.ids.staff_id.text,))]

            if password == entered_password and password != []:
                self.manager.current = "home"
            elif password != entered_password:
                raise exceptions.InvalidPasswordError
            elif password == [] and entered_password == []:
                raise exceptions.InvalidPasswordError

            self.ids.staff_id.text = ""
            self.ids.password.text = ""

        except exceptions.InvalidPasswordError:
            self.empty_class_dialog = MDDialog(
                title="Invalid Password!",
                text="Staff Id or Password is incorrect!",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="close", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def close_empty_class_dialog(self, obj):
        self.empty_class_dialog.dismiss()


class GreetUser(Screen):
    pass


class ForgotPassword(Screen):
    pass


class NewPassword(Screen):
    pass


class RegisterAccount(Screen):

    def register_account(self):
        try:
            if self.ids.first_name.text == '' or self.ids.surname.text == "" or self.ids.staff_id.text == "":
                raise exceptions.EmptyFieldError
            if self.ids.email.text == "" or self.ids.user_name.text == "" or self.ids.password.text == "":
                raise exceptions.EmptyFieldError
            if self.ids.reenter_password.text == "":
                raise exceptions.EmptyFieldError
            if self.ids.password.text != self.ids.reenter_password.text:
                raise exceptions.InvalidPasswordError
            the_date = datetime.datetime.today()
            self.date = the_date.replace(microsecond=0)

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""INSERT INTO users_account VALUES(:first_name, :surname, :full_name, :staff_id,
                            :email, :user_name, :password, :reenter_password, :date_registered,
                            :entered_password, :log_date)""",
                      {
                          'first_name': self.ids.first_name.text,
                          'surname': self.ids.surname.text,
                          'full_name': self.ids.first_name.text + " " + self.ids.surname.text,
                          'staff_id': self.ids.staff_id.text,
                          'email': self.ids.email.text,
                          'user_name': self.ids.user_name.text,
                          "password": self.ids.password.text,
                          "reenter_password": self.ids.reenter_password.text,
                          'date_registered': self.date,
                          'entered_password': '',
                          'log_date': self.date,

                      })
            conn.commit()
            self.ids.first_name.text = ''
            self.ids.surname.text = ""
            self.ids.staff_id.text = ""
            self.ids.email.text = ""
            self.ids.user_name.text = ""
            self.ids.password.text = ""
            self.ids.reenter_password.text = ""
        except exceptions.EmptyFieldError:
            self.empty_class_dialog = MDDialog(
                title="Empty Fields!",
                text="You have to fill in all the blanks",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="close", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        except exceptions.InvalidPasswordError:
            self.empty_class_dialog = MDDialog(
                title="Password Error!",
                text="Your passwords do not match",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="close", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        except sqlite3.IntegrityError:
            self.empty_class_dialog = MDDialog(
                title="ID Error!",
                text="Staff Id already exist in the Database",
                radius=[40, 7, 40, 7],
                buttons=[
                    MDRectangleFlatButton(
                        text="close", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

        else:
            self.empty_class_dialog = MDDialog(
                title="Congratulations!",
                text="You have successfully registerd a new account!",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="close", on_release=self.close_empty_class_dialog_and_change_screen
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def close_empty_class_dialog_and_change_screen(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "authorization"

    def close_empty_class_dialog(self, obj):
        self.empty_class_dialog.dismiss()


class ChangePassword(Screen):
    def change_password(self):
        try:
            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            staff_no = [r[0] for r in c.execute(
                """SELECT staff_id  FROM users_account WHERE staff_id = ?""", (self.ids.staff_id.text,))]
            associated_password = [r[0] for r in c.execute(
                """SELECT password FROM users_account
                    WHERE staff_id = ?
                    AND password = ? """, (self.ids.staff_id.text, self.ids.old_password.text,))]
            if self.ids.new_password.text != self.ids.repeat_new_password.text:
                raise exceptions.InvalidPasswordError
            if staff_no == [] or associated_password == []:
                raise exceptions.IDError

            c.execute("""UPDATE users_account
                SET password =?,
                reenter_password = ?
                WHERE staff_id = ?
                AND password = ?""", (self.ids.new_password.text, self.ids.new_password.text,
                                      self.ids.staff_id.text, self.ids.old_password.text))
            conn.commit()
            self.ids.staff_id.text = ""
            self.ids.old_password.text = ""
            self.ids.new_password.text = ""
            self.ids.repeat_new_password.text = ''
        except exceptions.InvalidPasswordError:
            self.empty_class_dialog = MDDialog(
                title="Password Error!",
                text="Your passwords do not match",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="close", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        except exceptions.IDError:
            self.empty_class_dialog = MDDialog(
                title="ID or Password Error!",
                text="Staff Id or Password does not exist in the Database",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="close", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        else:
            self.empty_class_dialog = MDDialog(
                title="Congratulations!",
                text="You have successfully changed your password!",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="close", on_release=self.close_empty_class_dialog_and_change_screen
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def close_empty_class_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_empty_class_dialog_and_change_screen(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "authorization"
