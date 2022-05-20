import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.picker import MDDatePicker
import sqlite3
from kivymd.theming import ThemeManager
from kivy.uix.spinner import Spinner
from kivymd.uix.filemanager import MDFileManager
import datetime
from kivymd.uix.dialog import MDDialog
import numpy as np
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt


class EmptyClassSpinnerError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class EmptyFieldError(Exception):
    pass


class ConfirmationDialog(Exception):
    pass


class DuplicateFeesError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class NoAmountError(Exception):
    pass


class IDError(Exception):
    pass


class SignitoryError(Exception):
    pass


class Logo(Screen):
    pass


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
                raise InvalidPasswordError
            elif password == [] and entered_password == []:
                raise InvalidPasswordError

            self.ids.staff_id.text = ""
            self.ids.password.text = ""

        except InvalidPasswordError:
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
                raise EmptyFieldError
            if self.ids.email.text == "" or self.ids.user_name.text == "" or self.ids.password.text == "":
                raise EmptyFieldError
            if self.ids.reenter_password.text == "":
                raise EmptyFieldError
            if self.ids.password.text != self.ids.reenter_password.text:
                raise InvalidPasswordError
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
        except EmptyFieldError:
            self.empty_class_dialog = MDDialog(
                title="Empty Fields!",
                text="You have to fill in all the blanks",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="close", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        except InvalidPasswordError:
            self.empty_class_dialog = MDDialog(
                title="Password Error!",
                text="Your passwords do not match",
                radius=[25, 7, 25, 7],
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
                radius=[25, 7, 25, 7],
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
                raise InvalidPasswordError
            if staff_no == [] or associated_password == []:
                raise IDError

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
        except InvalidPasswordError:
            self.empty_class_dialog = MDDialog(
                title="Password Error!",
                text="Your passwords do not match",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="close", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        except IDError:
            self.empty_class_dialog = MDDialog(
                title="ID or Password Error!",
                text="Staff Id or Password does not exist in the Database",
                radius=[25, 7, 25, 7],
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
                radius=[25, 7, 25, 7],
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


class Home(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class Fees(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class Paid(Screen):
    table = None
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT g_and_c FROM grade_and_category")]
    grades = values

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def view_paid_list(self):
        try:
            if self.ids.class_list_spinner.text == "Select class":
                raise EmptyClassSpinnerError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            data = [r[0:6] for r in c.execute("""SELECT full_name, registration_number, grade_and_category,status,
                    balance, last_payment FROM fees_payable WHERE fees_payable.balance <= 0.0 AND fees_payable.grade_and_category =?""",
                                              (self.ids.class_list_spinner.text,))]
            spaces = [("", '', "", '', "", ""), ]
            values = data + spaces
            if not self.table:
                self.table = MDDataTable(
                    size_hint=(0.8, 0.5),
                    pos_hint={"center_x": .5, "center_y": .5},
                    use_pagination=True,
                    column_data=[
                        ("Full Name", dp(25)),
                        ('Regis_no', dp(25)),
                        ('Class', dp(25)),
                        ('Status', dp(25)),
                        ("Balance GHC", dp(25)),
                        ("Last Payment GHC", dp(30)),
                    ],
                )
                self.table.row_data = values
                self.ids.box.add_widget(self.table)

            if not not self.table:
                self.table.row_data = values
            conn.close()
        except EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="Please select a class to continue",
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

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class Owing(Screen):
    table = None
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT g_and_c FROM grade_and_category")]
    grades = values

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def view_arrears_list(self):
        try:
            if self.ids.class_list_spinner.text == "Select class":
                raise EmptyClassSpinnerError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            data = [r[0:6] for r in c.execute("""SELECT full_name, registration_number, grade_and_category,status,
                    balance, last_payment FROM fees_payable WHERE fees_payable.balance > 0.0 AND fees_payable.grade_and_category =?""",
                                              (self.ids.class_list_spinner.text,))]
            spaces = [("", '', "", '', "", ""), ]
            values = data + spaces
            if not self.table:
                self.table = MDDataTable(
                    size_hint=(0.8, 0.5),
                    pos_hint={"center_x": .5, "center_y": .5},
                    use_pagination=True,
                    column_data=[
                        ("Full Name", dp(25)),
                        ('Regis_no', dp(25)),
                        ('Class', dp(25)),
                        ('Status', dp(25)),
                        ("Balance GHC", dp(25)),
                        ("Last Payment GHC", dp(30)),
                    ],
                )
                self.table.row_data = values
                self.ids.box.add_widget(self.table)

            if not not self.table:
                self.table.row_data = values
            conn.close()
        except EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="Please select a class to continue",
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

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class CompleteClassList(Screen):
    table = None
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT g_and_c FROM grade_and_category")]
    grades = values

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def view_complete_list(self):
        try:
            if self.ids.class_list_spinner.text == "Select class":
                raise EmptyClassSpinnerError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            data = [r[0:6] for r in c.execute("""SELECT full_name, registration_number, grade_and_category,status,
                    balance, last_payment FROM fees_payable WHERE fees_payable.grade_and_category =?""",
                                              (self.ids.class_list_spinner.text,))]
            spaces = [("", '', "", '', "", ""), ]
            values = data + spaces
            if not self.table:
                self.table = MDDataTable(
                    size_hint=(0.8, 0.5),
                    pos_hint={"center_x": .5, "center_y": .5},
                    use_pagination=True,
                    column_data=[
                        ("Full Name", dp(25)),
                        ('Regis_no', dp(25)),
                        ('Class', dp(25)),
                        ('Status', dp(25)),
                        ("Balance GHC", dp(25)),
                        ("Last Payment GHC", dp(30)),
                    ],
                )
                self.table.row_data = values
                self.ids.box.add_widget(self.table)

            if not not self.table:
                self.table.row_data = values
            conn.close()
        except EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="Please select a class to continue",
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

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class ExitedStudents(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class PaymentPlatform(Screen):
    grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    grades = [r[0]
              for r in c.execute("SELECT g_and_c FROM grade_and_category")]
    g_and_c = grades

    def update_names_spinner(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        names = [r[0]
                 for r in c.execute("""SELECT full_name FROM fees_payable WHERE
               fees_payable.grade_and_category = ?""", (self.ids.grade_and_category_spinner.text,))]
        names_list = names
        if self.ids.grade_and_category_spinner.text == self.ids.grade_and_category_spinner.text:
            self.ids.students_full_name_spinner.values = names_list
        conn.close()

    def show_registration_no(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()

        parameter_search = c.execute(
            """SELECT unique_id FROM fees_payable WHERE grade_and_category=?
            AND full_name=?""", (self.ids.grade_and_category_spinner.text,
                                 self.ids.students_full_name_spinner.text))
        for row in parameter_search:
            self.ids.registration_number_of_paying_student.text = f"Registration Number is {str(row[0])}"

    def transaction_confirmation(self):
        self.transaction_confirmation_dialog = MDDialog(
            title="Confirmation Alert!",
            text=f"Are you sure you want to make a transaction of GHC{self.ids.amt.text} for {self.ids.students_full_name_spinner.text}?",
            radius=[25, 7, 25, 7],
            auto_dismiss=False,
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.transact, on_press=self.close_transaction_confirmation_dialog
                ),
                MDFlatButton(
                    text="NO", on_release=self.close_transaction_confirmation_dialog
                ),
            ],
        )
        self.transaction_confirmation_dialog.open()

    def transact(self, obj):
        try:
            the_date = datetime.datetime.today()
            self.date = the_date.replace(microsecond=0)
            self.year = the_date.year
            self.month_nm = str(the_date.month)
            datetime_object = datetime.datetime.strptime(self.month_nm, "%m")
            self.month_name = datetime_object.strftime("%B")
            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""INSERT INTO fees_paid VALUES(:date, :year, :term, :grade_and_category, :full_name,
                        :payee_type, :payment_type, :amt, :name_of_payee, :recept_no, :current_grade)""",
                      {
                          'date': self.date,
                          'year': self.year,
                          'term': self.ids.select_term_spinner.text,
                          'grade_and_category': self.ids.grade_and_category_spinner.text,
                          'full_name': self.ids.students_full_name_spinner.text,
                          'payee_type': self.ids.select_payee_spinner.text,
                          'payment_type': self.ids.payment_type_spinner.text,
                          'amt': self.ids.amt.text,
                          'name_of_payee': self.ids.name_of_payee.text,
                          "recept_no": self.ids.receipt_no.text,
                          "current_grade": self.ids.grade_and_category_spinner.text,

                      })

            c.execute("""
                    UPDATE fees_payable
                    SET last_payment= ?
                    WHERE fees_payable.full_name= ?
                    """, (self.ids.amt.text, self.ids.students_full_name_spinner.text))

            c.execute("""
                    UPDATE fees_payable
                    SET balance = balance - last_payment
                    WHERE fees_payable.full_name= ?
                    """, (self.ids.students_full_name_spinner.text,))

            c.execute("""
                    UPDATE fees_payable
                    SET date_of_last_payment = ?
                    WHERE fees_payable.full_name= ?
                    """, (self.date, self.ids.students_full_name_spinner.text,))

            c.execute(
                """INSERT INTO income_and_expenditure VALUES (:income, :expenditure, :p_l, :month,
                :term, :year)""",
                {
                    'income': self.ids.amt.text,
                    'expenditure': 0,
                    'p_l': 0,
                    'month': self.month_name,
                    'term': self.ids.select_term_spinner.text,
                    'year': self.year, })
            # c.execute("""
            #         UPDATE income_and_expenditure
            #         SET income = ? """, (self.ids.amt.text,))

            if self.ids.grade_and_category_spinner.text == "Select Grade":
                raise EmptyClassSpinnerError
            elif self.ids.students_full_name_spinner.text == "Select Name":
                raise EmptyClassSpinnerError
            if self.ids.select_payee_spinner.text == "Select Payee":
                raise EmptyFieldError
            elif self.ids.payment_type_spinner.text == "Transaction Mode":
                raise EmptyFieldError
            elif self.ids.amt.text == '' or int(self.ids.amt.text) <= 0:
                raise NoAmountError
            elif self.ids.name_of_payee.text == '':
                raise AuthorizationError
            elif self.ids.receipt_no.text == '':
                raise AuthorizationError

        except EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="No option as been selected for either class or name of student",
                radius=[30, 7, 30, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        except EmptyFieldError:
            self.empty_class_dialog = MDDialog(
                title="Important!",
                text="Select payee type and transaction mode to transact",
                auto_dismiss=False,
                radius=[30, 7, 30, 7],
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        except NoAmountError:
            self.empty_class_dialog = MDDialog(
                title="Bad Transaction Alert!",
                text="Amount cannot be less than or equal to 0",
                auto_dismiss=False,
                radius=[25, 7, 25, 7],
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        except AuthorizationError:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="Please provide name of payee and receipt number to transact",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        else:
            conn.commit()
            self.empty_class_dialog = MDDialog(
                title="Success!",
                text=f"You have succesfully made a transaction",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

            self.ids.select_term_spinner.text = "Select Grade"
            self.ids.grade_and_category_spinner.text = "Select Grade"
            self.ids.students_full_name_spinner.text = "Select Name"
            self.ids.select_payee_spinner.text = "Select Payee"
            self.ids.payment_type_spinner.text = "Transaction Mode"
            self.ids.registration_number_of_paying_student.text = 'Registration number of selected student'
            self.ids.amt.text = ""
            self.ids.name_of_payee.text = ""
            self.ids.receipt_no.text = ""
            self.ids.select_term_spinner.background_color = .7, 0, 0, .9
            self.ids.grade_and_category_spinner.background_color = .7, 0, 0, .9
            self.ids.students_full_name_spinner.background_color = .7, 0, 0, .9
            self.ids.select_payee_spinner.background_color = .7, 0, 0, .9
            self.ids.payment_type_spinner.background_color = .7, 0, 0, .9

        # finally:
        #     conn.close()

    def close_empty_class_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_transaction_confirmation_dialog(self, obj):
        self.transaction_confirmation_dialog.dismiss()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class PaymentHistory(Screen):
    table = None
    grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT g_and_c FROM grade_and_category")]
    grades = values

    def update_names_spinner(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        names = [r[0]
                 for r in c.execute("""SELECT full_name FROM fees_payable WHERE
               grade_and_category = ?""", (self.ids.grade_and_category_spinner.text,))]
        names_by_class = names

        if self.ids.grade_and_category_spinner.text == self.ids.grade_and_category_spinner.text:
            self.ids.students_full_name_spinner.values = names_by_class

    def view_payment_history(self):
        try:
            if self.ids.grade_and_category_spinner.text == "Select class":
                raise EmptyClassSpinnerError
            if self.ids.students_full_name_spinner.text == "Select name":
                raise EmptyClassSpinnerError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            data = [r[0:6] for r in c.execute("""SELECT date_and_time, amt, payee_type, name_of_payee, recept_no, grade_and_category FROM fees_paid
            WHERE fees_paid.current_grade =? AND fees_paid.full_name = ?""",
                                              (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))]
            spaces = [(" ", " ", " ", " ", " ", " "), ]
            values = data + spaces
            if not self.table:
                self.table = MDDataTable(
                    size_hint=(0.8, 0.5),
                    pos_hint={"center_x": .5, "center_y": .5},
                    use_pagination=True,
                    column_data=[
                        ('Date of Payment', dp(44)),
                        ("Amt GHC", dp(20)),
                        ('Paid by', dp(20)),
                        ('Name of Payee', dp(25)),
                        ('Receipt No', dp(22)),
                        ('Payment grade', dp(30)),


                    ],
                    rows_num=9,
                )
                self.table.row_data = values
                self.ids.tables_box.add_widget(self.table)

            if not not self.table:
                self.table.row_data = values

            conn.close()
            # self.ids.grade_and_category_spinner.background_color = .7, 0, 0, .9
            # self.ids.grade_and_category_spinner.text = "Select Grade"
            # self.ids.students_full_name_spinner.background_color = .7, 0, 0, .9
            # self.ids.students_full_name_spinner.text = "Select Grade"
        except EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="Please select a class to continue",
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

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class Staff(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class RegisterStaffSecurity(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class StaffRegistrationForms(Screen):
    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def selected(self, file_name):
        try:
            self.ids.certificate_image.source = file_name[0]
        except:
            pass

    # def select_path(self, path):
    #     print(path)
    #     self.exit_manager()

    # def open_file_manager(self):
    #     self.file_manager_obj.show('/')

    # def exit_manager(self):
    #     self.file_manager_obj.close()

    # staff appointment dae
    def save_appointment_date(self, instance, value, date_range):
        self.ids.date_appointed.text = str(value)

    def cancel_appointment_date(self, instance, value):
        self.ids.date_appointed.text = "No date selected yet"

    def show_appointment_date(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.save_appointment_date,
                         on_cancel=self.cancel_appointment_date)
        date_dialog.open()

    # staff date of birth picker

    def on_save_dob(self, instance, value, date_range):
        self.ids.staff_dob.text = str(value)

    def on_cancel_dob(self, instance, value):
        self.ids.staff_dob.text = "No date selected yet"

    def show_staff_dob(self):
        date_dialog = MDDatePicker(year=1990, month=1, day=1)
        date_dialog.bind(on_save=self.on_save_dob,
                         on_cancel=self.on_cancel_dob)
        date_dialog.open()

    def register_staff(self):
        try:
            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""INSERT INTO staff VALUES(:staff_first_name, :staff_surname,
                            :staff_full_name, :staff_gender, :staff_id, :date_of_birth,
                            :qualification, :name_of_school, :position_assigned, :staff_phone_number,
                            :staff_email, :staff_type, :salary_grade, :current_salary, :date_appointed, :upload_certificate)""",
                      {
                          'staff_first_name': self.ids.staff_first_name.text,
                          'staff_surname': self.ids.staff_surname.text,
                          'staff_full_name': self.ids.staff_first_name.text + " " + self.ids.staff_surname.text,
                          'staff_gender': self.ids.staff_gender.text,
                          'staff_id': self.ids.staff_id.text,
                          'date_of_birth': self.ids.staff_dob.text,
                          'qualification': self.ids.qualification.text,
                          'name_of_school': self.ids.name_of_school.text,
                          'position_assigned': self.ids.position_assigned.text,
                          'staff_phone_number': self.ids.staff_phone_number.text,
                          'staff_email': self.ids.staff_email.text,
                          'staff_type': self.ids.staff_type_spinner.text,
                          'salary_grade': self.ids.salary_grade_spinner.text,
                          "current_salary": "",
                          'date_appointed': self.ids.date_appointed.text,
                          'upload_certificate': "",

                      })

            c.execute(
                """INSERT OR IGNORE INTO salary_payable(staff_full_name, staff_id, salary_grade)
                    SELECT staff_full_name, staff_id, salary_grade FROM staff
                    """)
            c.execute(
                """INSERT OR IGNORE INTO differentiated_salary_payable(full_name, staff_id)
                    SELECT staff_full_name, staff_id FROM staff
                    WHERE staff.salary_grade='Differentiated'""")
            c.execute("""
                    UPDATE salary_payable
                    SET salary=total_salary
                    FROM set_salary
                    WHERE set_salary.salary_grade=salary_payable.salary_grade
                    AND salary_payable.salary_grade= ? """,
                      (self.ids.salary_grade_spinner.text,))

            if self.ids.staff_first_name.text == '':
                raise EmptyFieldError
            if self.ids.staff_surname.text == '':
                raise EmptyFieldError
            elif self.ids.staff_gender.text == 'Gender':
                raise EmptyFieldError
            elif self.ids.staff_id.text == '':
                raise sqlite3.IntegrityError
            elif self.ids.staff_dob.text == '':
                raise EmptyFieldError
            elif self.ids.qualification.text == '':
                raise EmptyFieldError
            elif self.ids.salary_grade_spinner.text == 'Select salary grade':
                raise EmptyFieldError
            elif self.ids.position_assigned.text == "":
                raise EmptyFieldError
            elif self.ids.staff_email.text == "":
                raise EmptyFieldError
            elif self.ids.staff_phone_number.text == "":
                raise EmptyFieldError
            elif self.ids.date_appointed.text == "":
                raise EmptyFieldError

        except sqlite3.IntegrityError:
            self.duplicate_dialog = MDDialog(
                title="Staff Id Duplicate",
                text="Staff Id already exists",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_duplicate_dialog, on_press=self.empty_staff_id
                    ),
                    MDRectangleFlatButton(
                        text="EDIT", on_release=self.close_duplicate_dialog, on_press=self.empty_staff_id
                    ),
                ],
            )
            self.duplicate_dialog.open()
        except EmptyFieldError:
            self.imcomplete_dialog = MDDialog(
                title="Incomplete Registration!",
                radius=[25, 7, 25, 7],
                text="All fields are required",
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_imcomplete_dialog,
                    ),
                ],
            )
            self.imcomplete_dialog.open()
        else:
            conn.commit()
            self.successful_staff_regis_dialog = MDDialog(
                title="Success!",
                radius=[25, 7, 25, 7],
                text="Staff member has been successfully entered on to the payroll",
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_successful_staff_regis_dialog,
                    ),
                ],
            )
            self.successful_staff_regis_dialog.open()
            self.ids.staff_first_name.text = ''
            self.ids.staff_surname.text = ''
            self.ids.staff_gender.text = 'Gender'
            self.ids.staff_gender.background_color = .7, 0, 0, .9
            self.ids.staff_id.text = ''
            self.ids.staff_dob.text = ''
            self.ids.name_of_school.text = ""
            self.ids.qualification.text = ''
            self.ids.salary_grade_spinner.text = 'Select salary grade'
            self.ids.salary_grade_spinner.background_color = .7, 0, 0, .9
            self.ids.staff_type_spinner.text = "Select staff type"
            self.ids.staff_type_spinner.background_color = .7, 0, 0, .9
            self.ids.position_assigned.text = ""
            self.ids.staff_email.text = ""
            self.ids.staff_phone_number.text = ""
            self.ids.date_appointed.text = ""

        finally:
            conn.close()

    def close_duplicate_dialog(self, obj):
        self.duplicate_dialog.dismiss()

    def empty_staff_id(self, obj):
        self.ids.staff_id.text = " "
        self.ids.staff_id.required = True

    def close_successful_staff_regis_dialog(self, obj):
        self.successful_staff_regis_dialog.dismiss()

    def close_imcomplete_dialog(self, obj):
        self.imcomplete_dialog.dismiss()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class EditStaffSecurity(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class EditStaffDetails(Screen):
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT staff_type FROM staff_type")]
    the_staff_type = values

    def update_names_spinner(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        names = [r[0]
                 for r in c.execute("""SELECT staff_full_name FROM staff WHERE staff_type= ?""",
                                    (self.ids.select_staff_type_spinner.text,))]
        staff_names = names
        if self.ids.select_staff_type_spinner.text == self.ids.select_staff_type_spinner.text:
            self.ids.select_staff_name_spinner.values = staff_names

    def show_data_to_be_edited(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()

        first_name = [r[0] for r in c.execute("""SELECT  staff_first_name FROM staff WHERE
            staff.staff_type = ? AND staff.staff_full_name =?""", (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text))]

        surname = [r[0] for r in c.execute("""SELECT  staff_surname FROM staff WHERE
            staff.staff_type = ? AND staff.staff_full_name = ?""", (self.ids.select_staff_type_spinner.text,
                                                                    self.ids.select_staff_name_spinner.text,))]
        gender = [r[0] for r in c.execute("""SELECT  staff_gender FROM staff WHERE
            staff.staff_type = ? AND staff.staff_full_name = ? """, (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        dob = [r[0] for r in c.execute("""SELECT  date_of_birth FROM staff WHERE
            staff.staff_type = ? AND staff.staff_full_name = ? """, (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        staff_qualification = [r[0] for r in c.execute("""SELECT  qualification FROM staff WHERE
            staff.staff_type= ? AND staff.staff_full_name= ? """, (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        school = [r[0] for r in c.execute("""SELECT  name_of_school FROM staff WHERE
            staff.staff_type = ? AND staff.staff_full_name = ? """, (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        position = [r[0] for r in c.execute("""SELECT  position_assigned FROM staff WHERE
            staff.staff_type= ? AND staff.staff_full_name= ? """, (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        phone = [r[0] for r in c.execute("""SELECT  staff_phone_number FROM staff WHERE
            staff.staff_type = ? AND staff.staff_full_name = ?""", (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        email = [r[0] for r in c.execute("""SELECT  staff_email FROM staff WHERE
            staff.staff_type= ? AND staff.staff_full_name= ? """, (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        salary_category = [r[0] for r in c.execute("""SELECT  salary_grade FROM staff WHERE
            staff.staff_type= ? AND staff.staff_full_name= ?""", (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]

        for row in first_name:
            self.ids.staff_first_name.text = str(first_name[0])
        for row in surname:
            self.ids.staff_surname.text = str(surname[0])
        for row in gender:
            self.ids.staff_gender_spinner.text = str(gender[0])
        for row in dob:
            self.ids.staff_dob.text = str(dob[0])
        for row in staff_qualification:
            self.ids.qualification.text = str(staff_qualification[0])
        for row in school:
            self.ids.name_of_school.text = str(school[0])
        for row in position:
            self.ids.position_assigned.text = str(position[0])
        for row in phone:
            self.ids.staff_phone_number.text = str(phone[0])
        for row in email:
            self.ids.staff_email.text = str(email[0])
        for row in salary_category:
            self.ids.salary_grade_spinner.text = str(salary_category[0])

    def save_edited_info(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()

        c.execute("""
                    UPDATE staff
                    SET
                    staff_first_name=?,
                    staff_surname=?,
                    staff_full_name=?,
                    staff_gender=?,
                    date_of_birth=?,
                    qualification=?,
                    name_of_school=?,
                    position_assigned=?,
                    staff_phone_number=?,
                    staff_email=?,
                    salary_grade=?
                    WHERE staff.staff_type =? AND staff.staff_full_name= ?
                    """, (self.ids.staff_first_name.text,  self.ids.staff_surname.text, self.ids.staff_first_name.text + " " +
                          self.ids.staff_surname.text, self.ids.staff_gender_spinner.text, self.ids.staff_dob.text,
                          self.ids.qualification.text, self.ids.name_of_school.text,
                          self.ids.position_assigned.text, self.ids.staff_phone_number.text, self.ids.staff_email.text,
                          self.ids.salary_grade_spinner.text, self.ids.select_staff_type_spinner.text,
                          self.ids.select_staff_name_spinner.text))
        conn.commit()
        self.ids.staff_first_name.text = ''
        self.ids.staff_surname.text = ''
        self.ids.staff_dob.text = ''
        self.ids.qualification.text = ''
        self.ids.name_of_school.text = ''
        self.ids.position_assigned.text = ''
        self.ids.staff_phone_number.text = ''
        self.ids.staff_email.text = ''
        self.ids.staff_gender_spinner.text = 'Select Gender'
        self.ids.salary_grade_spinner.text = "Select Salary Grade"
        self.ids.select_staff_type_spinner.text = "Select Staff Type"
        self.ids.select_staff_name_spinner.text = "Select Staff Name"
        self.ids.select_staff_name_spinner.background_color = .7, 0, 0, .9
        self.ids.salary_grade_spinner.background_color = .7, 0, 0, .9
        self.ids.staff_gender_spinner.background_color = .7, 0, 0, .9
        self.ids.select_staff_type_spinner.background_color = .7, 0, 0, .9

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def on_save(self, instance, value, date_range):
        self.ids.staff_dob.text = str(value)

    def update_calendar(self, year, month, day):
        self.ids.staff_dob.text = str(year)

    def on_cancel(self, instance, value):
        self.ids.staff_dob.text = "Select date"

    def show_calendar(self):
        date_dialog = MDDatePicker(month=1, day=1, min_year=2000)
        date_dialog.bind(on_save=self.on_save,
                         on_cancel=self.on_cancel)
        date_dialog.open()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class ViewStaffDetails(Screen):
    staff_preview = None
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT staff_type FROM staff_type")]
    the_staff_type = values

    def update_names_spinner(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        names = [r[0]
                 for r in c.execute("""SELECT staff_full_name FROM staff WHERE staff_type= ?""",
                                    (self.ids.select_staff_type_spinner.text,))]
        staff_names = names
        if self.ids.select_staff_type_spinner.text == self.ids.select_staff_type_spinner.text:
            self.ids.select_staff_name_spinner.values = staff_names

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def view_staff(self):
        try:
            if self.ids.select_staff_name_spinner.text == "Select Staff Name":
                raise EmptyClassSpinnerError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()

            c.execute("""
                UPDATE staff_preview SET staff_data=staff_full_name FROM staff WHERE staff_preview.Data='Name'
                AND staff.staff_full_name=? """,
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=staff_gender FROM staff WHERE staff_preview.Data="Gender"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text, ))
            c.execute("""
                UPDATE staff_preview SET staff_data=staff_id FROM staff WHERE staff_preview.Data="Staff ID"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))

            c.execute("""
                UPDATE staff_preview SET staff_data=date_of_birth FROM staff WHERE staff_preview.Data="Date of Birth"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=certification FROM staff WHERE staff_preview.Data="Qualification"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=name_of_school FROM staff WHERE staff_preview.Data="Name of Institution Attended"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=position_assigned FROM staff WHERE staff_preview.Data="Position Assigned"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=staff_phone_number FROM staff WHERE staff_preview.Data="Phone Number"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=staff_email FROM staff WHERE staff_preview.Data="Email"
                 AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=salary_grade FROM staff WHERE staff_preview.Data="Salary Grade"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=current_salary FROM staff WHERE staff_preview.Data="Current Salary GHC"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=date_appointed FROM staff WHERE staff_preview.Data="Date Appointed"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))

            conn.commit()

            data = [r[0:16] for r in c.execute("SELECT * FROM staff_preview")]
            values = data

            if not self.staff_preview:
                self.staff_preview = MDDataTable(
                    size_hint=(0.8, 0.9),
                    size=(500, 500),
                    pos_hint={"center_x": .5, "center_y": .5},
                    use_pagination=True,
                    rows_num=9,
                    column_data=[
                        ("Data Type", dp(50)),
                        ('Staff Info', dp(90)),
                    ],
                )
                self.staff_preview.row_data = values
                self.ids.box.add_widget(self.staff_preview)
            if not not self.staff_preview:
                self.staff_preview.row_data = values
            else:
                self.ids.box.add_widget(self.staff_preview)

            self.ids.select_staff_type_spinner.text = "Select Staff Type"
            self.ids.select_staff_name_spinner.text = "Select Staff Name"

        except EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty fields!",
                text="Please select staff's category and staff's name to continue",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def close_empty_class_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class SetSalaryForm(Screen):
    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def set_staff_salary(self):
        the_date = datetime.datetime.today()
        self.date = the_date.replace(microsecond=0)

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE set_salary
                SET
                date_set= ?,
                base_salary= ?,
                studies= ?,
                honourarium= ?,
                motivation= ?,
                bonus= ?,
                ssnit_contibution= ?,
                income_tax= ?,
                welfare= ?,
                total_salary= ?
                WHERE set_salary.salary_grade=?
                """, (self.date, self.ids.base_salary.text,
                      self.ids.staff_studies.text, self.ids.honourarium.text,
                      self.ids.staff_motivation.text, self.ids.bonus.text,
                      self.ids.ssnit_contibution.text, self.ids.income_tax.text,
                      self.ids.staff_welfare.text, "", self.ids.select_salary_grade_spinner.text,))

        c.execute(
            """UPDATE set_salary
                SET total_salary=base_salary + studies + honourarium +
                motivation + bonus + ssnit_contibution + income_tax + welfare
            """)

        c.execute("""
                UPDATE salary_payable
                SET salary=total_salary
                FROM set_salary
                WHERE set_salary.salary_grade=salary_payable.salary_grade
                 """)
        c.execute("""
                UPDATE staff
                SET current_salary=total_salary
                FROM set_salary
                WHERE set_salary.salary_grade=staff.salary_grade
                 """)

        conn.commit()
        conn.close()

    def show_previous_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        search = c.execute(
            """SELECT total_salary FROM set_salary WHERE salary_grade=?
                """, (self.ids.select_salary_grade_spinner.text,))
        for row in search:
            self.ids.current_total.text = f"Current Total Salary is {row[0]}"
        conn.close()

    def show_current_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE set_salary
                SET
                base_salary= ?,
                studies= ?,
                honourarium= ?,
                motivation= ?,
                bonus= ?,
                ssnit_contibution= ?,
                income_tax= ?,
                welfare= ?,
                total_salary= ?
                WHERE set_salary.salary_grade=?
                """, (self.ids.base_salary.text,
                      self.ids.staff_studies.text, self.ids.honourarium.text,
                      self.ids.staff_motivation.text, self.ids.bonus.text,
                      self.ids.ssnit_contibution.text, self.ids.income_tax.text,
                      self.ids.staff_welfare.text, 0, self.ids.select_salary_grade_spinner.text,))
        c.execute(
            """UPDATE set_salary
                SET total_salary=base_salary + studies + honourarium +
                motivation + bonus + ssnit_contibution + income_tax + welfare
            """)
        search = c.execute(
            """SELECT total_salary FROM set_salary WHERE salary_grade=?
                """, (self.ids.select_salary_grade_spinner.text,))
        for row in search:
            self.ids.current_total.text = f"Current Total Salary is {row[0]}"
        conn.close()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class Expenditure(Screen):
    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def file_expense(self, obj):
        the_date = datetime.datetime.today()
        self.year = the_date.year
        self.date = the_date.replace(microsecond=0)
        self.month_nm = str(the_date.month)
        datetime_object = datetime.datetime.strptime(self.month_nm, "%m")
        self.month_name = datetime_object.strftime("%B")
        try:
            conn = sqlite3.connect("school.db")
            c = conn.cursor()

            c.execute("""INSERT INTO expenditure VALUES(:date, :year, :term, :purpose, :expenditure_amt,
                :purpose_description, :Authorised_by, :Signitory_1, :Signitory_2,
                :Signitory_3)""",
                      {
                          'date': self.date,
                          'year': self.year,
                          'term': self.ids.select_term_spinner.text,
                          'purpose': self.ids.purpose_of_expenditure_spinner.text,
                          'expenditure_amt': self.ids.expenditure_amt.text,
                          'purpose_description': self.ids.description_of_expense.text,
                          'Authorised_by': self.ids.authorised_by.text,
                          'Signitory_1': self.ids.first_signatory.text,
                          'Signitory_2': self.ids.second_signatory.text,
                          'Signitory_3': self.ids.third_signatory.text,

                      })
            c.execute(
                """INSERT INTO income_and_expenditure VALUES (:income, :expenditure, :p_l, :month,
                :term, :year)""",
                {
                    'income': 0,
                    'expenditure': self.ids.expenditure_amt.text,
                    'p_l': 0,
                    'month': self.month_name,
                    'term': self.ids.select_term_spinner.text,
                    'year': self.year, })
            if self.ids.purpose_of_expenditure_spinner.text == "Select Purpose":
                raise EmptyFieldError
            elif self.ids.authorised_by.text == " " or self.ids.authorised_by.text == "":
                raise AuthorizationError
            elif self.ids.first_signatory.text == " " or self.ids.first_signatory.text == "":
                raise SignitoryError
            elif self.ids.expenditure_amt.text == " " or int(self.ids.expenditure_amt.text) <= 0 or self.ids.expenditure_amt.text == "":
                raise NoAmountError

        except AuthorizationError:
            self.authorization_error_dialog = MDDialog(
                title="Authorization required!",
                text="The 'Authorised by' field cannot be blank",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_authorization_error_dialog,
                    ),
                ],
            )

            self.authorization_error_dialog.open()
        except SignitoryError:
            self.authorization_error_dialog = MDDialog(
                title="Signitory required!",
                radius=[30, 7, 30, 7],
                text="At least one signitory is required",
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_authorization_error_dialog,
                    ),
                ],
            )

            self.authorization_error_dialog.open()
        except EmptyFieldError:
            self.no_purpose_dialog = MDDialog(
                title="Purpose required?",
                radius=[30, 7, 30, 7],
                auto_dismiss=False,
                text="You have to select a purpose for expenditure",
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_no_purpose_dialog,
                    ),
                ],
            )

            self.no_purpose_dialog.open()
        except NoAmountError:
            self.no_amt_dialog = MDDialog(
                title="Bad Transaction Alert!",
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
                text="Amount cannot be less than or equal to 0",
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_no_amt_dialog,
                    ),
                ],
            )

            self.no_amt_dialog.open()
        else:
            conn.commit()
            self.ids.purpose_of_expenditure_spinner.text = "Purpose"
            self.ids.expenditure_amt.text = ''
            self.ids.description_of_expense.text = ''
            self.ids.authorised_by.text = ''
            self.ids.first_signatory.text = ""
            self.ids.second_signatory.text = ''
            self.ids.third_signatory.text = ''
            self.ids.purpose_of_expenditure_spinner.background_color = .7, 0, 0, .9
        finally:
            conn.close()

    def close_no_amt_dialog(self, obj):
        self.no_amt_dialog.dismiss()

    def close_no_purpose_dialog(self, obj):
        self.no_purpose_dialog.dismiss()

    def close_authorization_error_dialog(self, obj):
        self.authorization_error_dialog.dismiss()

    def confirm_expense(self):
        self.successful_transaction_dialog = MDDialog(
            title="Confirmation?",
            radius=[30, 7, 30, 7],
            text=f"Are you sure you want to file {self.ids.purpose_of_expenditure_spinner.text} expense of GHC{self.ids.expenditure_amt.text}?",
            buttons=[

                MDRectangleFlatButton(
                    text="YES", on_release=self.file_expense, on_press=self.close_successful_transaction_dialog),
                MDRectangleFlatButton(
                    text="NO", on_press=self.close_successful_transaction_dialog),
            ],
        )

        self.successful_transaction_dialog.open()

    def close_successful_transaction_dialog(self, obj):
        self.successful_transaction_dialog.dismiss()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class StudentsInformation(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class StudentRegistrationForm(Screen):
    grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_grades FROM grades")]
    grades = values

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def register_student(self):
        try:
            the_date = datetime.datetime.today()
            self.date = the_date.replace(microsecond=0)

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute(
                """INSERT INTO students VALUES(:first_name, :surname, :full_name, :student_gender,
                        :registration_number, :dob, :special_health_condition, :father_name,
                        :mother_name, :guardian_name, :parent_guardian_phone, :parent_guardian_email,
                        :parent_guardian_occupation, :date_admitted, :grade, :grade_category,
                        :grade_and_category_admitted_to, :current_class, :status, :completion_level, :completed_arrear)""",
                {
                    'first_name': self.ids.first_name.text,
                    'surname': self.ids.surname.text,
                    'full_name': self.ids.first_name.text + " " + self.ids.surname.text,
                    'student_gender': self.ids.student_gender_spinner.text,
                    'registration_number': self.ids.registration_number.text,
                    'dob': self.ids.dob.text,
                    'special_health_condition': self.ids.special_health_condition.text,
                    'father_name': self.ids.father_name.text,
                    'mother_name': self.ids.mother_name.text,
                    'guardian_name': self.ids.guardian_name.text,
                    'parent_guardian_phone': self.ids.parent_guardian_phone.text,
                    'parent_guardian_email': self.ids.parent_guardian_email.text,
                    'parent_guardian_occupation': self.ids.parent_guardian_occupation.text,
                    'date_admitted': self.date,
                    'grade': self.ids.grade_spinner.text,
                    'grade_category': self.ids.grade_category_spinner.text,
                    'grade_and_category_admitted_to': self.ids.grade_spinner.text + self.ids.grade_category_spinner.text,
                    'current_class': self.ids.grade_spinner.text + self.ids.grade_category_spinner.text,
                    'status': self.ids.status_spinner.text,
                    'completion_level': '',
                    'completed_arrear': '',

                })

            c.execute(
                """INSERT OR IGNORE INTO fees_payable(full_name, registration_number,
                    grade, grade_and_category, status) SELECT full_name, registration_number,
                    grade, grade_and_category_admitted_to, status FROM students
                    WHERE completion_level != 'c'""")

            c.execute("""
                    UPDATE fees_payable SET unique_id=registration_number""")

            c.execute("""
                        UPDATE fees_payable
                        SET balance=set_fees.total_without_boarding
                        FROM set_fees
                        WHERE fees_payable.status='Day'
                        AND fees_payable.grade=set_fees.grade
                        AND fees_payable.registration_number= ?
                        """, (self.ids.registration_number.text,))

            c.execute("""
                        UPDATE fees_payable
                        SET balance=set_fees.total_with_boarding
                        FROM set_fees
                        WHERE fees_payable.status='Boarding'
                        AND fees_payable.grade=set_fees.grade
                        AND fees_payable.registration_number= ?
                        """, (self.ids.registration_number.text,))

            c.execute(
                """UPDATE fees_payable
                        SET
                        start_term=start_of_term FROM set_fees
                        """)

            c.execute(
                """UPDATE fees_payable
                        SET
                        end_term=end_of_term FROM set_fees
                        """)
            conn.commit()
            if self.ids.first_name.text == '' or self.ids.surname.text == '' or self.ids.student_gender_spinner.text == "Select Gender":
                raise EmptyFieldError
            elif self.ids.registration_number.text == '' or self.ids.dob.text == '':
                raise EmptyFieldError
            elif self.ids.special_health_condition.text == '' or self.ids.mother_name.text == '':
                raise EmptyFieldError
            elif self.ids.father_name.text == '' and self.ids.guardian_name.text == '':
                raise EmptyFieldError
            elif self.ids.parent_guardian_phone.text == '' or self.ids.parent_guardian_email.text == '':
                raise EmptyFieldError
            elif self.ids.parent_guardian_occupation.text == "" or self.ids.grade_spinner.text == "Select class":
                raise EmptyFieldError
            elif self.ids.grade_category_spinner.text == "Select grade category":
                raise EmptyFieldError
            elif self.ids.status_spinner.text == "Select status":
                raise EmptyFieldError

        except sqlite3.IntegrityError:
            self.duplicate_dialog = MDDialog(
                title="Registration Number Duplicate",
                text="Registration number already exists",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="Edit", on_release=self.close_duplicate_dialog
                    ),
                    MDFlatButton(
                        text="CANCEL", on_release=self.close_duplicate_dialog
                    ),
                ],
            )
            self.duplicate_dialog.open()

        except EmptyFieldError:
            self.incomplete_dialog = MDDialog(
                title="Incomplete Registration",
                text="All fields are required",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="Edit", on_release=self.close_incomplete_dialog
                    ),
                    MDFlatButton(
                        text="CANCEL", on_release=self.close_incomplete_dialog
                    ),
                ],
            )
            self.incomplete_dialog.open()
        else:
            self.sucessful_registration_dialog = MDDialog(
                title="Successful Registration",
                text="Student successfully registered",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_sucessful_registration_dialog
                    ),
                ],
            )
            self.sucessful_registration_dialog.open()

            self.ids.first_name.text = ''
            self.ids.surname.text = ''
            self.ids.student_gender_spinner.text = "Select Gender"
            self.ids.registration_number.text = ''
            self.ids.dob.text = ''
            self.ids.special_health_condition.text = ''
            self.ids.father_name.text = ''
            self.ids.mother_name.text = ''
            self.ids.guardian_name.text = ''
            self.ids.parent_guardian_phone.text = ''
            self.ids.parent_guardian_email.text = ''
            self.ids.parent_guardian_occupation.text = ""
            self.ids.grade_spinner.text = "Select class"
            self.ids.grade_category_spinner.text = "Select grade category"
            self.ids.status_spinner.text = "Select status"

    def close_incomplete_dialog(self, obj):
        self.incomplete_dialog.dismiss()

    def close_duplicate_dialog(self, obj):
        self.duplicate_dialog.dismiss()

    def close_sucessful_registration_dialog(self, obj):
        self.sucessful_registration_dialog.dismiss()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class ViewStudentDetails(Screen):
    student_preview = None
    grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT g_and_c FROM grade_and_category")]
    grades = values

    def update_names_spinner(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        names = [r[0]
                 for r in c.execute("""SELECT full_name FROM students WHERE
               students.current_class= ?""", (self.ids.grade_and_category_spinner.text,))]
        all_names = names

        if self.ids.grade_and_category_spinner.text == self.ids.grade_and_category_spinner.text:
            self.ids.students_full_name_spinner.values = all_names

    def preview_students(self):
        try:
            if self.ids.grade_and_category_spinner.text == "Select Class" or self.ids.students_full_name_spinner.text == 'Select Name':
                raise EmptyClassSpinnerError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()

            c.execute("""
                UPDATE preview SET Student_data=full_name FROM students WHERE preview.Data='Name'
                AND students.current_class=? AND students.full_name=? """,
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=student_gender FROM students WHERE preview.Data="Gender"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=current_class FROM students WHERE preview.Data="Class"
                AND students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))

            c.execute("""
                UPDATE preview SET Student_data=registration_number FROM students WHERE preview.Data="Registration No"
                AND students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=status FROM students WHERE preview.Data="Accomodation Status"
                AND students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=dob FROM students WHERE preview.Data="Date of Birth"
                AND students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=special_health_condition FROM students WHERE preview.Data="Health Condition"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=father_name FROM students WHERE preview.Data="Father's Name"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=mother_name FROM students WHERE preview.Data="Mother's Name"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=guardian_name FROM students WHERE preview.Data="Guardian's Name"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=parent_guardian_phone FROM students WHERE preview.Data="Parent/Guardian's Phone"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=parent_guardian_email FROM students WHERE preview.Data="Parent/Guardian's Email"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=parent_guardian_occupation FROM students WHERE preview.Data="Parent/Guardian's Occupation"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=date_admitted FROM students WHERE preview.Data="Date Admitted"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data='Completed' FROM students WHERE preview.Data="Completion level" AND students.completion_level='c'
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data='Not Completed' FROM students WHERE preview.Data="Completion level" AND students.completion_level=''
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=grade_and_category_admitted_to FROM students WHERE preview.Data="Class Admitted to"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))

            conn.commit()

            data = [r[0:16] for r in c.execute("SELECT * FROM preview")]
            values = data

            if not self.student_preview:
                self.student_preview = MDDataTable(
                    size_hint=(0.8, 0.9),
                    size=(500, 500),
                    pos_hint={"center_x": .5, "center_y": .5},
                    use_pagination=True,
                    rows_num=9,
                    column_data=[
                        ("Data Type", dp(50)),
                        ('Student Info', dp(90)),
                    ],
                )
                self.student_preview.row_data = values
                self.ids.box.add_widget(self.student_preview)
            if not not self.student_preview:
                self.student_preview.row_data = values

            else:
                self.ids.box.add_widget(self.student_preview)

            self.ids.grade_and_category_spinner.text = "Select Class"
            self.ids.grade_and_category_spinner.background_color = .7, 0, 0, .9

            self.ids.students_full_name_spinner.text = "Select Name"
            self.ids.students_full_name_spinner.background_color = .7, 0, 0, .9

        except EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty fields!",
                text="Please select student's class and student's name to continue",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def close_empty_class_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_table(self):
        if self.student_preview:
            self.ids.grade_and_category_spinner.text = "Select Class"
            self.ids.students_full_name_spinner.text = "Select Name"

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class EditStudentsDetails(Screen):
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values1 = [r[0]
               for r in c.execute("SELECT available_grades FROM grades")]
    grades = values1

    values2 = [r[0]
               for r in c.execute("SELECT g_and_c FROM grade_and_category")]
    grades_and_category = values2

    def update_names_spinner(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        names = [r[0]
                 for r in c.execute("""SELECT full_name FROM students WHERE
               students.current_class= ? """, (self.ids.grade_and_category_spinner.text,))]
        names_by_class = names
        if self.ids.grade_and_category_spinner.text == self.ids.grade_and_category_spinner.text:
            self.ids.students_full_name_spinner.values = names_by_class

    def show_data_to_be_edited(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()

        name = [r[0] for r in c.execute("""SELECT  first_name FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]

        surname = [r[0] for r in c.execute("""SELECT  surname FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        student_gender = [r[0] for r in c.execute("""SELECT  student_gender FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        dob = [r[0] for r in c.execute("""SELECT  dob FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        special_health_condition = [r[0] for r in c.execute("""SELECT  special_health_condition FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        father_name = [r[0] for r in c.execute("""SELECT  father_name FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        mother_name = [r[0] for r in c.execute("""SELECT  mother_name FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        guardian_name = [r[0] for r in c.execute("""SELECT  guardian_name FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        parent_guardian_phone = [r[0] for r in c.execute("""SELECT  parent_guardian_phone FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        parent_guardian_email = [r[0] for r in c.execute("""SELECT  parent_guardian_email FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        parent_guardian_occupation = [r[0] for r in c.execute("""SELECT  parent_guardian_occupation FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        grade = [r[0] for r in c.execute("""SELECT  grade FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        grade_category = [r[0] for r in c.execute("""SELECT  grade_category FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        status = [r[0] for r in c.execute("""SELECT  status FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]

        for row in name:
            self.ids.first_name.text = str(name[0])
        for row in surname:
            self.ids.surname.text = str(surname[0])
        for row in student_gender:
            self.ids.student_gender_spinner.text = str(student_gender[0])
        for row in dob:
            self.ids.dob.text = str(dob[0])
        for row in special_health_condition:
            self.ids.special_health_condition.text = str(
                special_health_condition[0])
        for row in father_name:
            self.ids.father_name.text = str(father_name[0])
        for row in mother_name:
            self.ids.mother_name.text = str(mother_name[0])
        for row in guardian_name:
            self.ids.guardian_name.text = str(guardian_name[0])
        for row in parent_guardian_phone:
            self.ids.parent_guardian_phone.text = str(parent_guardian_phone[0])
        for row in parent_guardian_email:
            self.ids.parent_guardian_email.text = str(parent_guardian_email[0])
        for row in parent_guardian_occupation:
            self.ids.parent_guardian_occupation.text = str(
                parent_guardian_occupation[0])
        for row in name:
            self.ids.grade_spinner.text = str(grade[0])
        for row in name:
            self.ids.grade_category_spinner.text = str(grade_category[0])
        for row in name:
            self.ids.status_spinner.text = str(status[0])

    def save_edited_info(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""
                    UPDATE students
                    SET first_name = ?,
                    surname =?,
                    full_name = ?,
                    student_gender =?,
                    dob =?,
                    special_health_condition  =?,
                    father_name =?,
                    mother_name =?,
                    guardian_name =?,
                    parent_guardian_phone =?,
                    parent_guardian_email =?,
                    parent_guardian_occupation =?,
                    grade =?,
                    grade_category =?,
                    status =?,
                    current_class = ?
                    WHERE students.current_class= ? AND students.full_name =?
                    """, (self.ids.first_name.text,  self.ids.surname.text, self.ids.first_name.text + " " +
                          self.ids.surname.text, self.ids.student_gender_spinner.text, self.ids.dob.text,
                          self.ids.special_health_condition.text, self.ids.father_name.text,
                          self.ids.mother_name.text, self.ids.guardian_name.text, self.ids.parent_guardian_phone.text,
                          self.ids.parent_guardian_email.text, self.ids.parent_guardian_occupation.text,
                          self.ids.grade_spinner.text, self.ids.grade_category_spinner.text,
                          #   self.ids.grade_spinner.text + self.ids.grade_category_spinner.text,
                          self.ids.status_spinner.text, self.ids.grade_spinner.text +
                          self.ids.grade_category_spinner.text,
                          self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text))
        c.execute("""
                    UPDATE fees_payable
                    SET full_name = ?,
                    grade = ?,
                    grade_and_category = ?  WHERE fees_payable.grade_and_category= ? AND fees_payable.full_name =? """,
                  (self.ids.first_name.text + " " + self.ids.surname.text, self.ids.grade_spinner.text,
                   self.ids.grade_spinner.text +
                   self.ids.grade_category_spinner.text, self.ids.grade_and_category_spinner.text,
                   self.ids.students_full_name_spinner.text))
        conn.commit()

        self.ids.first_name.required = False
        self.ids.first_name.text = ''
        self.ids.surname.text = ''
        self.ids.student_gender_spinner.text = 'Select Gender'
        self.ids.dob.text = ''
        self.ids.special_health_condition.text = ''
        self.ids.father_name.text = ''
        self.ids.mother_name.text = ''
        self.ids.guardian_name.text = ''
        self.ids.parent_guardian_phone.text = ''
        self.ids.parent_guardian_email.text = ''
        self.ids.parent_guardian_occupation.text = ''
        self.ids.grade_spinner.text = 'Select Grade'
        self.ids.grade_category_spinner.text = 'Select Grade Category'
        self.ids.status_spinner.text = 'Select Status'
        self.ids.grade_and_category_spinner.text = 'Select Class'
        self.ids.students_full_name_spinner.text = 'Select Name'
        self.ids.grade_and_category_spinner.background_color = .7, 0, 0, .9
        self.ids.students_full_name_spinner.background_color = .7, 0, 0, .9
        self.ids.status_spinner.background_color = .7, 0, 0, .9
        self.ids.grade_category_spinner.background_color = .7, 0, 0, .9
        self.ids.grade_spinner.background_color = .7, 0, 0, .9
        self.ids.student_gender_spinner.background_color = .7, 0, 0, .9

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def on_save(self, instance, value, date_range):
        self.ids.dob.text = str(value)

    def update_calendar(self, year, month, day):
        self.ids.dob.text = str(year)

    def on_cancel(self, instance, value):
        self.ids.dob.text = "Select date"

    def show_calendar(self):
        date_dialog = MDDatePicker(month=1, day=1, min_year=2000)
        date_dialog.bind(on_save=self.on_save,
                         on_cancel=self.on_cancel)
        date_dialog.open()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class ExitedStudents(Screen):
    # grade_spinner = Spinner()
    grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    year = [r[0]
            for r in c.execute("SELECT available_years FROM years")]
    # year_completed = values

    def update_exited_pupils(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        completed_final_years = [r[0]
                                 for r in c.execute("""SELECT full_name FROM exited_students WHERE
               exited_students.exited_year = ?""", (self.ids.year_exited_spinner.text,))]
        form3_list = completed_final_years
        if self.ids.year_exited_spinner.text == self.ids.year_exited_spinner.text:
            self.ids.students_full_name_spinner.values = form3_list

    def preview_exited_students(self):
        pass


class CompletedStudents(Screen):
    student_preview = None
    grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_years FROM years")]
    year_completed = values

    def update_completed_pupils(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        completed_final_years = [r[0]
                                 for r in c.execute("""SELECT full_name FROM completed_students WHERE
               completed_students.completed_year = ?""", (self.ids.year_completed_spinner.text,))]
        form3_list = completed_final_years
        if self.ids.year_completed_spinner.text == self.ids.year_completed_spinner.text:
            self.ids.students_full_name_spinner.values = form3_list

    def preview_completed_students(self):
        try:
            if self.ids.year_completed_spinner.text == "Select Year Completed" or self.ids.students_full_name_spinner.text == 'Select Name':
                raise EmptyClassSpinnerError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()

            c.execute("""
                UPDATE preview SET Student_data = full_name FROM students WHERE preview.Data = 'Name'
                AND students.current_class =? AND students.full_name=? """,
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = student_gender FROM students WHERE preview.Data = "Gender"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = current_class FROM students WHERE preview.Data = "Class"
                AND students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))

            c.execute("""
                UPDATE preview SET Student_data = registration_number FROM students WHERE preview.Data = "Registration No"
                AND students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = status FROM students WHERE preview.Data = "Accomodation Status"
                AND students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = dob FROM students WHERE preview.Data = "Date of Birth"
                AND students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = special_health_condition FROM students WHERE preview.Data = "Health Condition"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = father_name FROM students WHERE preview.Data = "Father's Name"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = mother_name FROM students WHERE preview.Data = "Mother's Name"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = guardian_name FROM students WHERE preview.Data = "Guardian's Name"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = parent_guardian_phone FROM students WHERE preview.Data = "Parent/Guardian's Phone"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = parent_guardian_email FROM students WHERE preview.Data = "Parent/Guardian's Email"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = parent_guardian_occupation FROM students WHERE preview.Data = "Parent/Guardian's Occupation"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = date_admitted FROM students WHERE preview.Data = "Date Admitted"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = 'Completed' FROM students WHERE preview.Data = "Completion level" AND students.completion_level = 'c'
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = grade_and_category FROM students WHERE preview.Data = "Class Admitted to"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=completed_arrear FROM students WHERE preview.Data="Arrears"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            conn.commit()

            data = [r[0:17] for r in c.execute("SELECT * FROM preview")]
            values = data

            if not self.student_preview:
                self.student_preview = MDDataTable(
                    size_hint=(0.8, 0.9),
                    size=(500, 500),
                    pos_hint={"center_x": .5, "center_y": .5},
                    use_pagination=True,
                    rows_num=9,
                    column_data=[
                        ("Data Type", dp(50)),
                        ('Student Info', dp(90)),
                    ],
                )
                self.student_preview.row_data = values
                self.ids.box.add_widget(self.student_preview)
            if not not self.student_preview:
                self.student_preview.row_data = values
                self.ids.students_full_name_spinner.text = "Select Name"
                self.ids.students_full_name_spinner.text = "Select Name"
            else:
                self.ids.box.add_widget(self.student_preview)

        except EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty fields!",
                text="Please select student's class and student's name to continue",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def close_empty_class_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class Info(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class Manage(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class Set(Screen):
    def confirmation_of_promotion_dialog(self):
        self.confirmation_promotion_dialog = MDDialog(
            title="Warning!",
            text="Clicking 'YES' will move all students to the next grade. Grade 9 students will be removed from the fees list. They can be added back using the 'Reverse Promotion' only once!",
            radius=[40, 7, 40, 7],
            auto_dismiss=False,
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.promote_students
                ),
                MDFlatButton(
                    text="NO", on_release=self.close_confirmation_promotion_dialog
                ),
            ],
        )
        self.confirmation_promotion_dialog.open()

    def close_confirmation_promotion_dialog(self, obj):
        self.confirmation_promotion_dialog.dismiss()

    def promote_students(self, obj):
        completed_date = datetime.date.today()
        self.completed_year = completed_date.year
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("UPDATE completed_students SET completed_year = ?",
                  (self.completed_year,))
        c.execute(
            "UPDATE completed_students SET completion_level = '#'")
        conn.commit()
        conn.close()
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """INSERT OR IGNORE INTO completed_students(full_name, registration_number,
                grade, grade_and_category, status, arrears)
                SELECT full_name, registration_number,
                grade, grade_and_category, status, balance FROM fees_payable
                WHERE grade = 'Grade 9'
                """)
        c.execute(
            "UPDATE completed_students SET completed_year = ? WHERE completion_level = 'o'",
            (self.completed_year,))
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            "UPDATE completed_students SET completion_level = 'o' WHERE completion_level = 'o'")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            "UPDATE completed_students SET completion_level = 'c' WHERE completion_level = 'o'")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE students
                SET completion_level = 'c'
                FROM completed_students
                WHERE completed_students.registration_number = students.registration_number
                """)
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE students
                SET completed_arrear = arrears
                FROM completed_students
                WHERE completed_students.registration_number = students.registration_number
                """)
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """DELETE FROM fees_payable WHERE grade = 'Grade 9'""")
        c.execute("""UPDATE fees_paid
        SET grade_and_category = 'Completed A' WHERE grade_and_category = 'Grade 9A'""")
        c.execute("""UPDATE fees_paid
        SET grade_and_category = 'Completed B' WHERE grade_and_category = 'Grade 9B'""")
        c.execute("""UPDATE students
        SET current_class = ? WHERE current_class = 'Grade 9A'""", (self.completed_year,))
        c.execute("""UPDATE students
        SET current_class = ? WHERE current_class = 'Grade 9B'""", (self.completed_year,))
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
        SET grade = 'Grade 9' WHERE grade = 'Grade 8'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 9A' WHERE grade_and_category = 'Grade 8A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 9B' WHERE grade_and_category = 'Grade 8B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 9A' WHERE current_grade = 'Grade 8A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 9B' WHERE current_grade = 'Grade 8B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 9A' WHERE current_class = 'Grade 8A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 9B' WHERE current_class = 'Grade 8B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 9' WHERE grade = 'Grade 8'""")
        # c.execute("""UPDATE students
        # SET grade = 'Grade 3' WHERE grade = 'Grade 2'""")
        # # c.execute("""UPDATE students
        # SET current_class = 'Grade 9B' WHERE current_class = 'Grade 8B'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'Grade 8' WHERE grade = 'Grade 7'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 8A' WHERE grade_and_category = 'Grade 7A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 8B' WHERE grade_and_category = 'Grade 7B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 8A' WHERE current_grade = 'Grade 7A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 8B' WHERE current_grade = 'Grade 7B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 8A' WHERE current_class = 'Grade 7A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 8B' WHERE current_class = 'Grade 7B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 8' WHERE grade = 'Grade 7'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'Grade 7' WHERE grade = 'Grade 6'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 7A' WHERE grade_and_category = 'Grade 6A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 7B' WHERE grade_and_category = 'Grade 6B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 7A' WHERE current_grade = 'Grade 6A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 7B' WHERE current_grade = 'Grade 6B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 7A' WHERE current_class = 'Grade 6A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 7B' WHERE current_class = 'Grade 6B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 7' WHERE grade = 'Grade 6'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'Grade 6' WHERE grade = 'Grade 5'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 6A' WHERE grade_and_category = 'Grade 5A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 6B' WHERE grade_and_category = 'Grade 5B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 6A' WHERE current_grade = 'Grade 5A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 6B' WHERE current_grade = 'Grade 5B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 6A' WHERE current_class = 'Grade 5A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 6B' WHERE current_class = 'Grade 5B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 6' WHERE grade = 'Grade 5'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'Grade 5' WHERE grade = 'Grade 4'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 5A' WHERE grade_and_category = 'Grade 4A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 5B' WHERE grade_and_category = 'Grade 4B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 5A' WHERE current_grade = 'Grade 4A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 5B' WHERE current_grade = 'Grade 4B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 5A' WHERE current_class = 'Grade 4A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 5B' WHERE current_class = 'Grade 4B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 5' WHERE grade = 'Grade 4'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
                SET grade = 'Grade 4' WHERE grade = 'Grade 3'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 4A' WHERE grade_and_category = 'Grade 3A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 4B' WHERE grade_and_category = 'Grade 3B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 4A' WHERE current_grade = 'Grade 3A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 4B' WHERE current_grade = 'Grade 3B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 4A' WHERE current_class = 'Grade 3A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 4B' WHERE current_class = 'Grade 3B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 4' WHERE grade = 'Grade 3'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'Grade 3' WHERE grade = 'Grade 2'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 3A' WHERE grade_and_category = 'Grade 2A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 3B' WHERE grade_and_category = 'Grade 2B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 3A' WHERE current_grade = 'Grade 2A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 3B' WHERE current_grade = 'Grade 2B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 3A' WHERE current_class = 'Grade 2A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 3B' WHERE current_class = 'Grade 2B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 3' WHERE grade = 'Grade 2'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'Grade 2' WHERE grade = 'Grade 1'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 2A' WHERE grade_and_category = 'Grade 1A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 2B' WHERE grade_and_category = 'Grade 1B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 2A' WHERE current_grade = 'Grade 1A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 2B' WHERE current_grade = 'Grade 1B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 2A' WHERE current_class = 'Grade 1A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 2B' WHERE current_class = 'Grade 1B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 2' WHERE grade = 'Grade 1'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'Grade 1' WHERE grade = 'KG 2'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 1A' WHERE grade_and_category = 'KG 2A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 1B' WHERE grade_and_category = 'KG 2B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 1A' WHERE current_grade = 'KG 2A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 1B' WHERE current_grade = 'KG 2B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 1A' WHERE current_class = 'KG 2A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 1B' WHERE current_class = 'KG 2B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 1' WHERE grade = 'KG 2'""")
        # c.execute("""UPDATE students
        # SET grade = 'Grade 1' WHERE current_class = 'KG 2B'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE fees_payable SET grade = 'KG 2' WHERE grade = 'KG 1'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'KG 2A' WHERE grade_and_category = 'KG 1A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'KG 2B' WHERE grade_and_category = 'KG 1B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'KG 2A' WHERE current_grade = 'KG 1A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'KG 2B' WHERE current_grade = 'KG 1B'""")
        c.execute("""UPDATE students
        SET current_class = 'KG 2A' WHERE current_class = 'KG 1A'""")
        c.execute("""UPDATE students
        SET current_class = 'KG 2B' WHERE current_class = 'KG 1B'""")
        c.execute("""UPDATE students
        SET grade = 'KG 2' WHERE grade = 'KG 1'""")
        conn.commit()
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
                SET grade = 'KG 1' WHERE grade = 'Nursery 2'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'KG 1A' WHERE grade_and_category = 'Nursery 2A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'KG 1B' WHERE grade_and_category = 'Nursery 2B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'KG 1A' WHERE current_grade = 'Nursery 2A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'KG 1B' WHERE current_grade = 'Nursery 2B'""")
        c.execute("""UPDATE students
        SET current_class = 'KG 1A' WHERE current_class = 'Nursery 2A'""")
        c.execute("""UPDATE students
        SET current_class = 'KG 1B' WHERE current_class = 'Nursery 2B'""")
        c.execute("""UPDATE students
        SET grade = 'KG 1' WHERE grade = 'Nursery 2'""")
        # c.execute("""UPDATE students
        # SET grade = 'KG 1B' WHERE grade = 'Nursery 2B'""")

        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
        SET grade = 'Nursery 2' WHERE grade = 'Nursery 1'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Nursery 2A' WHERE grade_and_category = 'Nursery 1A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Nursery 2B' WHERE grade_and_category = 'Nursery 1B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Nursery 2A' WHERE current_grade = 'Nursery 1A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Nursery 2B' WHERE current_grade = 'Nursery 1B'""")
        c.execute("""UPDATE students
        SET current_class = 'Nursery 2A' WHERE current_class = 'Nursery 1A'""")
        c.execute("""UPDATE students
        SET current_class = 'Nursery 2B' WHERE current_class = 'Nursery 1B'""")
        c.execute("""UPDATE students
        SET grade = 'Nursery 2' WHERE grade = 'Nursery 1'""")
        # c.execute("""UPDATE students
        # SET grade = 'Nursery 2' WHERE grade = 'Nursery 1B'""")

        conn.commit()
        conn.close()
        self.confirmation_promotion_dialog.dismiss()

    def successful_promotion(self):
        self.successful_promotion_dialog = MDDialog(
            title="Successful Promotion!",
            text="All students have been successfully promoted to the next class",
            radius=[40, 7, 40, 7],
            auto_dismiss=False,
            buttons=[
                MDRectangleFlatButton(
                    text="CLOSE", on_release=self.close_successful_promotion_dialog
                ),
            ],
        )
        self.successful_promotion_dialog.open()

    def close_successful_promotion_dialog(self, obj):
        self.successful_promotion_dialog.dismiss()

    def confirmation_of_demotion_dialog(self):
        self.confirmation_demotion_dialog = MDDialog(
            title="Warning!",
            text="Clicking 'YES' will move all students a grade back",
            radius=[25, 7, 25, 7],
            auto_dismiss=False,
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.reverse_promotion
                ),
                MDRectangleFlatButton(
                    text="NO", on_release=self.close_successful_demotion_dialog
                ),
            ],
        )
        self.confirmation_demotion_dialog.open()

    def reverse_promotion(self, obj):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE fees_payable SET grade = 'Nursery 1' WHERE grade = 'Nursery 2'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Nursery 1A' WHERE grade_and_category = 'Nursery 2A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Nursery 1B' WHERE grade_and_category = 'Nursery 2B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Nursery 1A' WHERE current_grade = 'Nursery 2A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Nursery 1B' WHERE current_grade = 'Nursery 2B'""")
        c.execute("""UPDATE students
        SET current_class = 'Nursery 1A' WHERE current_class = 'Nursery 2A'""")
        c.execute("""UPDATE students
        SET current_class = 'Nursery 1B' WHERE current_class = 'Nursery 2B'""")
        c.execute("""UPDATE students
        SET grade = 'Nursery 1' WHERE grade = 'Nursery 2'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
                SET grade = 'Nursery 2' WHERE grade = 'KG 1'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Nursery 2A' WHERE grade_and_category = 'KG 1A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Nursery 2B' WHERE grade_and_category = 'KG 1B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Nursery 2A' WHERE current_grade = 'KG 1A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Nursery 2B' WHERE current_grade = 'KG 1B'""")
        c.execute("""UPDATE students
        SET current_class = 'Nursery 2A' WHERE current_class = 'KG 1A'""")
        c.execute("""UPDATE students
        SET current_class = 'Nursery 2B' WHERE current_class = 'KG 1B'""")
        c.execute("""UPDATE students
        SET grade = 'Nursery 2' WHERE grade = 'KG 1'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE fees_payable SET grade = 'KG 1' WHERE grade = 'KG 2'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'KG 1A' WHERE grade_and_category = 'KG 2A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'KG 1B' WHERE grade_and_category = 'KG 2B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'KG 1A' WHERE current_grade = 'KG 2A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'KG 1B' WHERE current_grade = 'KG 2B'""")
        c.execute("""UPDATE students
        SET current_class = 'KG 1A' WHERE current_class = 'KG 2A'""")
        c.execute("""UPDATE students
        SET current_class = 'KG 1B' WHERE current_class = 'KG 2B'""")
        c.execute("""UPDATE students
        SET grade = 'KG 1' WHERE grade = 'KG 2'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'KG 2' WHERE grade = 'Grade 1'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'KG 2A' WHERE grade_and_category = 'Grade 1A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'KG 2B' WHERE grade_and_category = 'Grade 1B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'KG 2A' WHERE current_grade = 'Grade 1A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'KG 2B' WHERE current_grade = 'Grade 1B'""")
        c.execute("""UPDATE students
        SET current_class = 'KG 2A' WHERE current_class = 'Grade 1A'""")
        c.execute("""UPDATE students
        SET current_class = 'KG 2B' WHERE current_class = Grade 1B""")
        c.execute("""UPDATE students
        SET grade = 'KG 2' WHERE grade = 'Grade 1'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'Grade 1' WHERE grade = 'Grade 2'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 1A' WHERE grade_and_category = 'Grade 2A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 1B' WHERE grade_and_category = 'Grade 2B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 1A' WHERE current_grade = 'Grade 2A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 1B' WHERE current_grade = 'Grade 2B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 1A' WHERE current_class = 'Grade 2A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 1B' WHERE current_class = 'Grade 2B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 1' WHERE grade = 'Grade 2'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'Grade 2' WHERE grade = 'Grade 3'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 2A' WHERE grade_and_category = 'Grade 3A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 2B' WHERE grade_and_category = 'Grade 3B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 2A' WHERE current_grade = 'Grade 3A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 2B' WHERE current_grade = 'Grade 3B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 2A' WHERE current_class = 'Grade 3A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 2B' WHERE current_class = 'Grade 3B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 2' WHERE grade = 'Grade 3'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
                SET grade = 'Grade 3' WHERE grade = 'Grade 4'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 3A' WHERE grade_and_category = 'Grade 4A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 3B' WHERE grade_and_category = 'Grade 4B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 3A' WHERE current_grade = 'Grade 4A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 3B' WHERE current_grade = 'Grade 4B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 3A' WHERE current_class = 'Grade 4A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 3B' WHERE current_class = 'Grade 4B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 3' WHERE grade = 'Grade 4'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
                SET grade = 'Grade 4' WHERE grade = 'Grade 5'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 4A' WHERE grade_and_category = 'Grade 5A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 4B' WHERE grade_and_category = 'Grade 5B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 4A' WHERE current_grade = 'Grade 5A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 4B' WHERE current_grade = 'Grade 5B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 4A' WHERE current_class = 'Grade 5A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 4B' WHERE current_class = 'Grade 5B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 4' WHERE grade = 'Grade 5'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'Grade 5' WHERE grade = 'Grade 6'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 5A' WHERE grade_and_category = 'Grade 6A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 5B' WHERE grade_and_category = 'Grade 6B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 5A' WHERE current_grade = 'Grade 6A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 5B' WHERE current_grade = 'Grade 6B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 5A' WHERE current_class = 'Grade 6A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 5B' WHERE current_class = 'Grade 6B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 5' WHERE grade = 'Grade 6'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'Grade 6' WHERE grade = 'Grade 7'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 6A' WHERE grade_and_category = 'Grade 7A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 6B' WHERE grade_and_category = 'Grade 7B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 6A' WHERE current_grade = 'Grade 7A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 6B' WHERE current_grade = 'Grade 7B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 6A' WHERE current_class = 'Grade 7A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 6B' WHERE current_class = 'Grade 7B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 6' WHERE grade = 'Grade 7'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
            SET grade = 'Grade 7' WHERE grade = 'Grade 8'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 7A' WHERE grade_and_category = 'Grade 8A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 7B' WHERE grade_and_category = 'Grade 8B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 7A' WHERE current_grade = 'Grade 8A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 7B' WHERE current_grade = 'Grade 8B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 7A' WHERE current_class = 'Grade 8A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 7B' WHERE current_class = 'Grade 8B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 7' WHERE grade = 'Grade 8'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_payable
        SET grade = 'Grade 8' WHERE grade = 'Grade 9'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 8A' WHERE grade_and_category = 'Grade 9A'""")
        c.execute("""UPDATE fees_payable
        SET grade_and_category = 'Grade 8B' WHERE grade_and_category = 'Grade 9B'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 8A' WHERE current_grade = 'Grade 9A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 8B' WHERE current_grade = 'Grade 9B'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 8A' WHERE current_class = 'Grade 9A'""")
        c.execute("""UPDATE students
        SET current_class = 'Grade 8B' WHERE current_class = 'Grade 9B'""")
        c.execute("""UPDATE students
        SET grade = 'Grade 8' WHERE grade = 'Grade 9'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 9A' WHERE current_grade = 'Completed A'""")
        c.execute("""UPDATE fees_paid
        SET current_grade = 'Grade 9B' WHERE current_grade = 'Completed B'""")
        c.execute(
            """INSERT OR IGNORE INTO fees_payable(full_name, registration_number, grade, grade_and_category,
                    status, balance)
                SELECT full_name, registration_number, grade, grade_and_category, status, arrears
                FROM completed_students
                WHERE completed_students.completion_level = 'c'""")
        conn.commit()
        conn.close()

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """DELETE FROM completed_students WHERE completed_students.completion_level = 'c'""")
        conn.commit()
        conn.close()

        self.confirmation_demotion_dialog.dismiss()

    def successful_demotion(self):
        self.successful_demotion_dialog = MDDialog(
            title="Successful grade reversal!",
            text="All students have been successfully reversed back to their previous class",
            radius=[25, 7, 25, 7],
            auto_dismiss=False,
            buttons=[
                MDRectangleFlatButton(
                    text="close", on_release=self.close_successful_demotion_dialog
                ),
            ],
        )
        self.successful_demotion_dialog.open()

    def close_successful_demotion_dialog(self, obj):
        self.successful_demotion_dialog.dismiss()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout
                ),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class SetSecuritykey(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class SetTerm(Screen):
    def on_save_start(self, instance, value, date_range):
        self.ids.start_date_of_term.text = str(value)

    def on_cancel_start(self, instance, value):
        self.ids.start_date_of_term.text = "Start of term date not selected"

    def show_start_date(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_start,
                         on_cancel=self.on_cancel_start)
        date_dialog.open()

    def on_save_end(self, instance, value, date_range):
        self.ids.end_date_of_term.text = str(value)

    def on_cancel_end(self, instance, value):
        self.ids.end_date_of_term.text = "End of term date not selected"

    def show_end_date(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_end,
                         on_cancel=self.on_cancel_end)
        date_dialog.open()

    def set_term(self):
        try:
            if self.ids.start_date_of_term.text == "Start of Term" or self.ids.end_date_of_term.text == "  End of Term  ":
                raise EmptyFieldError
            if self.ids.select_term_spinner.text == "Select Term":
                raise EmptyClassSpinnerError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()

            c.execute(
                """UPDATE set_fees
                    SET
                    start_of_term = ?,
                    end_of_term = ?
                    """, (self.ids.start_date_of_term.text, self.ids.end_date_of_term.text,))
            c.execute(
                """UPDATE fees_payable
                    SET
                    start_term = ?,
                    end_term = ?
                    """, (self.ids.start_date_of_term.text, self.ids.end_date_of_term.text,))

        except EmptyFieldError:
            self.term_selection_dialog = MDDialog(
                title="Warning!",
                text="Start of term and end of term must be selected.",
                radius=[40, 7, 40, 7],
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_term_selection_dialog,
                    ),
                ],
            )
            self.term_selection_dialog.open()
        except EmptyClassSpinnerError:
            self.term_selection_dialog = MDDialog(
                title="Empty!",
                text="Please select the term to proceed",
                radius=[40, 7, 40, 7],
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_term_selection_dialog,
                    ),
                ],
            )
            self.term_selection_dialog.open()
        else:
            conn.commit()
            self.success_term_selection_dialog = MDDialog(
                title="Success!",
                text=f"You have selected {self.ids.start_date_of_term.text} to {self.ids.end_date_of_term.text} as term dates",
                radius=[40, 7, 40, 7],
                buttons=[
                    MDRectangleFlatButton(
                        text="NEXT", on_release=self.close_success_term_selection_dialog,
                    ),
                ],
            )
            self.success_term_selection_dialog.open()

    def close_term_selection_dialog(self, obj):
        self.term_selection_dialog.dismiss()

    def close_success_term_selection_dialog(self, obj):
        self.success_term_selection_dialog.dismiss()
        self.manager.current = "set"

    def set_term_dialog(self):
        self.term_dialog = MDDialog(
            title="Confirm",
            text="Are you sure you want to set term?",
            radius=[25, 7, 25, 7],
            auto_dismiss=False,
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.set_term, on_press=self.close_term_dialog
                ),
            ],
        )
        self.term_dialog.open()

    def close_term_dialog(self, obj):
        self.term_dialog.dismiss()

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class SetFeesClassSelection(Screen):
    grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_grades FROM grades")]
    grades = values

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class DifferentiatedSalary(Screen):
    def show_staff_names(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        names = [r[0] for r in c.execute(
            "SELECT full_name FROM differentiated_salary_payable")]
        if self.ids.reset_staff_name_spinner.text == "Yes":
            self.ids.select_staff_name_spinner.values = names
        else:
            self.ids.select_staff_name_spinner.values = ["Select Staff Name"]

    def set_differentiated_salary_dialog(self):
        self.differentiated_salary_dialog = MDDialog(
            title="Confirm",
            text="Are you sure you want to set salary?",
            buttons=[
                MDRectangleFlatButton(
                    text="close", on_release=self.set_differentiated_salary
                ),
            ],
        )
        self.differentiated_salary_dialog.open()

    def close_differentiated_salary_dialog(self, obj):
        self.differentiated_salary_dialog.dismiss()

    def set_differentiated_salary(self):
        try:
            the_date = datetime.datetime.today()
            self.date = the_date.replace(microsecond=0)
            if self.ids.reset_staff_name_spinner.text == "Reset Differentiated Salary":
                raise EmptyFieldError
            if self.ids.select_staff_name_spinner.text == "Select Staff Name":
                raise EmptyFieldError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()

            c.execute(
                """UPDATE differentiated_salary_payable
                    SET
                    date_set = ?,
                    base_salary = ?,
                    studies = ?,
                    honourarium = ?,
                    motivation = ?,
                    bonus = ?,
                    ssnit_contibution = ?,
                    income_tax = ?,
                    welfare = ?,
                    total_salary = ?
                    WHERE differentiated_salary_payable.full_name=?
                    """, (self.date, self.ids.base_salary.text,
                          self.ids.staff_studies.text, self.ids.honourarium.text,
                          self.ids.staff_motivation.text, self.ids.bonus.text,
                          self.ids.ssnit_contibution.text, self.ids.income_tax.text,
                          self.ids.staff_welfare.text, 0, self.ids.select_staff_name_spinner.text,))
            c.execute(
                """UPDATE differentiated_salary_payable
                    SET total_salary = base_salary + studies + honourarium +
                    motivation + bonus - ssnit_contibution - income_tax + welfare
                """)
            c.execute(
                """UPDATE salary_payable
                    SET salary = total_salary
                    FROM differentiated_salary_payable
                    WHERE differentiated_salary_payable.full_name = salary_payable.staff_full_name
                """)

        except EmptyFieldError:
            self.incomplete_dialog = MDDialog(
                title="Empty Fields",
                text="Select a reset option, and name of the differentiated staff member",
                buttons=[
                    MDRectangleFlatButton(
                        text="Edit", on_release=self.close_incomplete_dialog
                    ),
                    MDFlatButton(
                        text="CANCEL", on_release=self.close_incomplete_dialog
                    ),
                ],
            )
            self.incomplete_dialog.open()

        else:
            conn.commit()
            self.ids.base_salary.text = ""
            self.ids.staff_studies.text = ""
            self.ids.honourarium.text = ""
            self.ids.staff_motivation.text = ""
            self.ids.bonus.text = ""
            self.ids.ssnit_contibution.text = ""
            self.ids.income_tax.text = ""
            self.ids.staff_welfare.text = ""
            self.ids.reset_staff_name_spinner.text = "Reset Differentiated Salary"
            self.ids.reset_staff_name_spinner.background_color = .7, 0, 0, .9
            self.ids.select_staff_name_spinner.text = "Select Staff Name"
            self.ids.select_staff_name_spinner.background_color = .7, 0, 0, .9
            self.ids.previous_total.text = "Previous total salary shows here"
            self.ids.current_total.text = "Current total salary shows here"
            self.successful_transaction_dialog = MDDialog(
                title="Success!",
                text=f"You have set a new salary for {self.ids.select_staff_name_spinner.text}",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_successful_transaction_dialog)
                ],
            )

            self.successful_transaction_dialog.open()

    def close_successful_transaction_dialog(self, obj):
        self.successful_transaction_dialog.dismiss()

    def show_current_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()

        c.execute(
            """UPDATE differentiated_salary_payable
                SET
                base_salary = ?,
                studies = ?,
                honourarium = ?,
                motivation = ?,
                bonus = ?,
                ssnit_contibution = ?,
                income_tax = ?,
                welfare = ?,
                total_salary = ?
                WHERE differentiated_salary_payable.full_name=?
                """, (self.ids.base_salary.text,
                      self.ids.staff_studies.text, self.ids.honourarium.text,
                      self.ids.staff_motivation.text, self.ids.bonus.text,
                      self.ids.ssnit_contibution.text, self.ids.income_tax.text,
                      self.ids.staff_welfare.text, 0, self.ids.select_staff_name_spinner.text,))
        c.execute(
            """UPDATE differentiated_salary_payable
                SET total_salary = base_salary + studies + honourarium +
                motivation + bonus - ssnit_contibution - income_tax + welfare
            """)
        parameter_search = c.execute(
            """SELECT total_salary FROM differentiated_salary_payable WHERE full_name=?
                """, (self.ids.select_staff_name_spinner.text,))
        for row in parameter_search:
            self.ids.current_total.text = f"GHC{row[0]}"
        conn.close()

    def show_previous_total(self):
        the_date = datetime.datetime.today()
        self.date = the_date.replace(microsecond=0)
        conn = sqlite3.connect("school.db")
        c = conn.cursor()

        parameter_search = c.execute(
            """SELECT total_salary FROM differentiated_salary_payable WHERE full_name=?
                """, (self.ids.select_staff_name_spinner.text,))
        for row in parameter_search:
            self.ids.previous_total.text = f"GHC{row[0]}"
        conn.close()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class FeesBreakdown(Screen):
    grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_grades FROM grades")]
    grades = values

    def show_previous_fees_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        parameter_search = c.execute(
            """SELECT total_with_boarding FROM set_fees WHERE grade=?
                """, (self.ids.select_level_grade_spinner.text,))
        for row in parameter_search:
            self.ids.previous_fees_total.text = f"GHC{row[0]}"
        conn.close()

    def show_previous_fees_w_o_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        parameter_search = c.execute(
            """SELECT total_without_boarding FROM set_fees WHERE grade=?
                """, (self.ids.select_level_grade_spinner.text,))
        for row in parameter_search:
            self.ids.previous_fees_w_o_boarding_total.text = f"GHC{row[0]}"
        conn.close()

    def show_current_fees_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE set_fees
                SET
                tuition = ?,
                studies = ?,
                pta_levy = ?,
                printing = ?,
                maintenance = ?,
                motivation = ?,
                library = ?,
                canteen = ?,
                sanitation = ?,
                sports = ?,
                boarding_fees = ?
                WHERE set_fees.grade=?
                """, (self.ids.tuition.text, self.ids.studies.text, self.ids.pta_levy.text,
                      self.ids.printing.text, self.ids.maintenance.text, self.ids.motivation.text,
                      self.ids.library.text, self.ids.can_teen.text, self.ids.sanitation.text,
                      self.ids.sports.text, self.ids.boarding_fees.text,
                      self.ids.select_level_grade_spinner.text,))

        c.execute(
            """UPDATE set_fees
                SET total_with_boarding = tuition + studies + pta_levy + printing +
                maintenance + motivation + library + canteen + sanitation + sports +
                boarding_fees""")

        parameter_search = c.execute(
            """SELECT total_with_boarding FROM set_fees WHERE grade=?
                """, (self.ids.select_level_grade_spinner.text,))
        for row in parameter_search:
            self.ids.current_fee_total.text = f"GHC{row[0]}"
        conn.close()

    def show_current_fees_w_o_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE set_fees
                SET
                tuition = ?,
                studies = ?,
                pta_levy = ?,
                printing = ?,
                maintenance = ?,
                motivation = ?,
                library = ?,
                canteen = ?,
                sanitation = ?,
                sports = ?,
                boarding_fees = ?
                WHERE set_fees.grade=?
                """, (self.ids.tuition.text, self.ids.studies.text, self.ids.pta_levy.text,
                      self.ids.printing.text, self.ids.maintenance.text, self.ids.motivation.text,
                      self.ids.library.text, self.ids.can_teen.text, self.ids.sanitation.text,
                      self.ids.sports.text, self.ids.boarding_fees.text,
                      self.ids.select_level_grade_spinner.text,))

        c.execute(
            """UPDATE set_fees
                SET total_without_boarding = tuition + studies + pta_levy +
                printing + maintenance + motivation + library + canteen +
                sanitation + sports
            """)

        parameter_search = c.execute(
            """SELECT total_without_boarding FROM set_fees WHERE grade=?
                """, (self.ids.select_level_grade_spinner.text,))
        for row in parameter_search:
            self.ids.current_fee_w_o_boarding_total.text = f"GHC{row[0]}"
        conn.close()

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def taking_fees_to_(self):
        pass

    def confirm_set_fees(self):
        self.confirm_set_fees_dialog = MDDialog(
            title="Confirmation!",
            text=f"Do you want to set fees for {self.ids.select_level_grade_spinner.text}?",
            radius=[40, 7, 40, 7],
            auto_dismiss=False,
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_press=self.set_fees, on_release=self.close_confirm_set_fees_dialog
                ),
                MDFlatButton(
                    text="NO", on_release=self.close_confirm_set_fees_dialog
                )
            ],
        )

        self.confirm_set_fees_dialog.open()

    def close_confirm_set_fees_dialog(self, obj):
        self.confirm_set_fees_dialog.dismiss()

    def set_fees(self, obj):
        the_date = datetime.datetime.today()
        self.date = the_date.replace(microsecond=0)
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        print(self.ids.select_term_spinner.text)
        c.execute(
            """UPDATE set_fees SET total_without_boarding = 0.0, total_with_boarding = 0.0
                WHERE set_fees.term != ?""", (self.ids.select_term_spinner.text,))
        conn.commit()
        total_without_boarding = [r[0] for r in c.execute("""SELECT total_without_boarding FROM set_fees
                WHERE grade =?""", (self.ids.select_level_grade_spinner.text,))]
        total_with_boarding = [r[0] for r in c.execute("""SELECT total_with_boarding FROM set_fees
                WHERE grade =?""", (self.ids.select_level_grade_spinner.text,))]
        try:
            if total_without_boarding != 0.0 and total_with_boarding != 0.0:
                raise DuplicateFeesError
            c.execute(
                """UPDATE set_fees
                    SET
                    tuition = ?,
                    studies = ?,
                    pta_levy = ?,
                    printing = ?,
                    maintenance = ?,
                    motivation = ?,
                    library = ?,
                    canteen = ?,
                    sanitation = ?,
                    sports = ?,
                    boarding_fees = ?,
                    time_set = ?
                    WHERE set_fees.grade=?
                    """, (self.ids.tuition.text,
                          self.ids.studies.text, self.ids.pta_levy.text, self.ids.printing.text,
                          self.ids.maintenance.text, self.ids.motivation.text, self.ids.library.text,
                          self.ids.can_teen.text, self.ids.sanitation.text, self.ids.sports.text,
                          self.ids.boarding_fees.text, self.date,
                          self.ids.select_level_grade_spinner.text, self.ids.select_term_spinner.text))

            c.execute(
                """UPDATE set_fees
                    SET total_without_boarding = tuition + studies + pta_levy +
                    printing + maintenance + motivation + library + canteen +
                    sanitation + sports
                """)

            c.execute(
                """UPDATE set_fees
                    SET total_with_boarding = tuition + studies + pta_levy + printing +
                    maintenance + motivation + library + canteen + sanitation + sports +
                    boarding_fees""")

            c.execute("""
                    UPDATE fees_payable
                    SET balance = balance + set_fees.total_without_boarding
                    FROM set_fees
                    WHERE set_fees.grade = fees_payable.grade
                    AND fees_payable.grade = ?
                    AND fees_payable.status = 'Day'""",
                      (self.ids.select_level_grade_spinner.text,))

            c.execute("""
                    UPDATE fees_payable
                    SET balance = balance + set_fees.total_with_boarding
                    FROM set_fees
                    WHERE set_fees.grade = fees_payable.grade
                    AND fees_payable.grade = ?
                    AND fees_payable.status = 'Boarding'""",
                      (self.ids.select_level_grade_spinner.text,))
            c.execute(
                """INSERT INTO set_fees_history VALUES (:time_set, :term, :grade, :tuition,
                :studies, :pta_levy, :printing, :maintenance, :motivation, :library, :canteen,
                :sanitation, :sports, :boarding_fees, :total_without_boarding,
                :total_with_boarding)""",
                {
                    'time_set': self.date,
                    'term': self.ids.select_term_spinner.text,
                    'grade': self.ids.select_level_grade_spinner.text,
                    'tuition': self.ids.tuition.text,
                    'studies': self.ids.studies.text,
                    'pta_levy': self.ids.pta_levy.text,
                    'printing': self.ids.printing.text,
                    'maintenance': self.ids.maintenance.text,
                    'motivation': self.ids.motivation.text,
                    'library': self.ids.library.text,
                    'canteen': self.ids.can_teen.text,
                    'sanitation': self.ids.sanitation.text,
                    'sports': self.ids.sports.text,
                    'boarding_fees': self.ids.boarding_fees.text,
                    'total_without_boarding': "",
                    'total_with_boarding': "",



                })

            c.execute(
                """UPDATE set_fees_history
                    SET total_without_boarding = tuition + studies + pta_levy +
                    printing + maintenance + motivation + library + canteen +
                    sanitation + sports
                """)

            c.execute(
                """UPDATE set_fees_history
                    SET total_with_boarding = tuition + studies + pta_levy + printing +
                    maintenance + motivation + library + canteen + sanitation + sports +
            boarding_fees""")

        except DuplicateFeesError:
            self.duplicate_fees_dialog = MDDialog(
                title="Warning!",
                text=f"You have already set fees for {self.ids.select_level_grade_spinner.text} ",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_duplicate_fees_dialog
                    )
                ],
            )

            self.duplicate_fees_dialog.open()
        else:
            conn.commit()
            self.successful_fees_setting_dialog = MDDialog(
                title="Success!",
                text=f"You have successfully set fees for {self.ids.select_level_grade_spinner.text} ",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_successful_fees_setting_dialog
                    )
                ],
            )

            self.successful_fees_setting_dialog.open()

    def close_successful_fees_setting_dialog(self, obj):
        self.successful_fees_setting_dialog.dismiss()

    def close_duplicate_fees_dialog(self, obj):
        self.duplicate_fees_dialog.dismiss()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class Analytics(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class Figures(Screen):
    table = None
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_years FROM years")]
    years = values

    def get_table(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE income_and_expenditure SET p_l = income - expenditure""")
        conn.commit()
        jan = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'January'
                AND income_and_expenditure_previews.month_preview = 'January'""",
                        (self.ids.select_year_spinner.text,))
        feb = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'February'
                AND income_and_expenditure_previews.month_preview = 'February'""",
                        (self.ids.select_year_spinner.text,))
        mar = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'March'
                AND income_and_expenditure_previews.month_preview = 'March'""",
                        (self.ids.select_year_spinner.text,))
        apr = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'April'
                AND income_and_expenditure_previews.month_preview = 'April'""",
                        (self.ids.select_year_spinner.text,))
        may = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'May'
                AND income_and_expenditure_previews.month_preview = 'May'""",
                        (self.ids.select_year_spinner.text,))
        june = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'June'
                AND income_and_expenditure_previews.month_preview = 'June'""",
                         (self.ids.select_year_spinner.text,))
        july = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'July'
                AND income_and_expenditure_previews.month_preview = 'July'""",
                         (self.ids.select_year_spinner.text,))
        august = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'August'
                AND income_and_expenditure_previews.month_preview = 'August'""",
                           (self.ids.select_year_spinner.text,))
        sep = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'September'
                AND income_and_expenditure_previews.month_preview = 'September'""",
                        (self.ids.select_year_spinner.text,))
        october = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'october'
                AND income_and_expenditure_previews.month_preview = 'october'""",
                            (self.ids.select_year_spinner.text,))
        nov = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'November'
                AND income_and_expenditure_previews.month_preview = 'November'""",
                        (self.ids.select_year_spinner.text,))
        dec = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'December'
                AND income_and_expenditure_previews.month_preview = 'December'""",
                        (self.ids.select_year_spinner.text,))
        conn.commit()
        if self.ids.select_term_spinner.text == "Yearly":
            try:
                if self.ids.select_year_spinner.text == "Select Year":
                    raise EmptyClassSpinnerError
                if self.ids.select_term_spinner.text == "Select Term":
                    raise EmptyClassSpinnerError

                data = [r[0:6] for r in c.execute("""SELECT year_preview, term_preview, month_preview,
                        income_preview, expenditure_preview, p_l_preview
                        FROM income_and_expenditure_previews""",)]

                spaces = [(" ", " ", " ", " ", " ", ""), ]
                values = data + spaces

                if not self.table:
                    self.table = MDDataTable(
                        size_hint=(0.8, 0.5),
                        size=(400, 300),
                        pos_hint={"center_x": .5, "center_y": .5},
                        use_pagination=True,
                        column_data=[
                            ('Year', dp(20)),
                            ('Term', dp(25)),
                            ('Month', dp(25)),
                            ("Income", dp(25)),
                            ('Expenditure', dp(25)),
                            ('Surplus/Loss', dp(30)),

                        ],
                        rows_num=9,
                    )
                    self.table.row_data = values
                    self.ids.box.add_widget(self.table)

                if not not self.table:
                    self.table.row_data = values

            except EmptyClassSpinnerError:
                self.empty_spinner_dialog = MDDialog(
                    title="Warning!",
                    text="Please select the year and term to proceed",
                    radius=[40, 7, 40, 7],
                    auto_dismiss=False,
                    buttons=[
                        MDRectangleFlatButton(
                            text="CLOSE", on_release=self.close_empty_spinner_dialog
                        ),

                    ],
                )
                self.empty_spinner_dialog.open()

        else:
            # self.ids.select_term_spinner.text == "First Term":
            try:
                if self.ids.select_year_spinner.text == "Select Year":
                    raise EmptyClassSpinnerError
                if self.ids.select_term_spinner.text == "Select Term":
                    raise EmptyClassSpinnerError

                data = [r[0:6] for r in c.execute("""SELECT year_preview, term_preview, month_preview,
                        income_preview, expenditure_preview, p_l_preview
                        FROM income_and_expenditure_previews
                        WHERE income_and_expenditure_previews.term_preview =?
                        AND income_and_expenditure_previews.year_preview = ?""",
                                                  (self.ids.select_term_spinner.text, self.ids.select_year_spinner,))]
                print(data)
                spaces = [(" ", " ", " ", " ", " ", ""), ]
                values = data + spaces
                if not self.table:
                    self.table = MDDataTable(
                        size_hint=(0.8, 0.5),
                        size=(400, 300),
                        pos_hint={"center_x": .5, "center_y": .5},
                        use_pagination=True,
                        column_data=[
                            ('Year', dp(20)),
                            ('Term', dp(25)),
                            ('Month', dp(25)),
                            ("Income", dp(25)),
                            ('Expenditure', dp(25)),
                            ('Surplus/Loss', dp(30)),

                        ],
                        rows_num=9,
                    )
                    self.table.row_data = values
                    self.ids.box.add_widget(self.table)

                if not not self.table:
                    self.table.row_data = values
            except EmptyClassSpinnerError:
                self.empty_spinner_dialog = MDDialog(
                    title="Warning!",
                    text="Please select the year and term to proceed",
                    radius=[40, 7, 40, 7],
                    auto_dismiss=False,
                    buttons=[
                        MDRectangleFlatButton(
                            text="CLOSE", on_release=self.close_empty_spinner_dialog
                        ),

                    ],
                )
                self.empty_spinner_dialog.open()

        # elif self.ids.select_term_spinner.text == "Second Term":
        #     try:
        #         if self.ids.select_year_spinner.text == "Select Year":
        #             raise EmptyClassSpinnerError
        #         if self.ids.select_term_spinner.text == "Select Term":
        #             raise EmptyClassSpinnerError

        #         data = [r[0:6] for r in c.execute("""SELECT year_preview, term_preview, month_preview,
        #                 income_preview, expenditure_preview, p_l_preview
        #                 FROM income_and_expenditure_previews
        #                 WHERE income_and_expenditure_previews.term_preview =?
        #                 AND income_and_expenditure_previews.year_preview = ?""",
        #                                           (self.ids.select_term_spinner.text, self.ids.select_year_spinner))]

        #         spaces = [(" ", " ", " ", " ", " ", ""), ]
        #         values = data + spaces
        #         if not self.table:
        #             self.table = MDDataTable(
        #                 size_hint=(0.8, 0.5),
        #                 size=(400, 300),
        #                 pos_hint={"center_x": .5, "center_y": .5},
        #                 use_pagination=True,
        #                 column_data=[
        #                     ('Year', dp(20)),
        #                     ('Term', dp(25)),
        #                     ('Month', dp(25)),
        #                     ("Income", dp(25)),
        #                     ('Expenditure', dp(25)),
        #                     ('Surplus/Loss', dp(30)),

        #                 ],
        #                 rows_num=9,
        #             )
        #             self.table.row_data = values
        #             self.ids.box.add_widget(self.table)

        #         if not not self.table:
        #             self.table.row_data = values
        #     except EmptyClassSpinnerError:
        #         self.empty_spinner_dialog = MDDialog(
        #             title="Warning!",
        #             text="Please select the year and term to proceed",
        #             radius=[40, 7, 40, 7],
        #             auto_dismiss=False,
        #             buttons=[
        #                 MDRectangleFlatButton(
        #                     text="CLOSE", on_release=self.close_empty_spinner_dialog
        #                 ),

        #             ],
        #         )
        #         self.empty_spinner_dialog.open()
        # elif self.ids.select_term_spinner.text == "Third Term":
        #     try:
        #         if self.ids.select_year_spinner.text == "Select Year":
        #             raise EmptyClassSpinnerError
        #         if self.ids.select_term_spinner.text == "Select Term":
        #             raise EmptyClassSpinnerError

        #         data = [r[0:6] for r in c.execute("""SELECT year_preview, term_preview, month_preview,
        #                 income_preview, expenditure_preview, p_l_preview
        #                 FROM income_and_expenditure_previews
        #                 WHERE income_and_expenditure_previews.term_preview =?
        #                 AND income_and_expenditure_previews.year_preview = ?""",
        #                                           (self.ids.select_term_spinner.text, self.ids.select_year_spinner))]

        #         spaces = [(" ", " ", " ", " ", " ", ""), ]
        #         values = data + spaces
        #         if not self.table:
        #             self.table = MDDataTable(
        #                 size_hint=(0.8, 0.5),
        #                 size=(400, 300),
        #                 pos_hint={"center_x": .5, "center_y": .5},
        #                 use_pagination=True,
        #                 column_data=[
        #                     ('Year', dp(20)),
        #                     ('Term', dp(25)),
        #                     ('Month', dp(25)),
        #                     ("Income", dp(25)),
        #                     ('Expenditure', dp(25)),
        #                     ('Surplus/Loss', dp(30)),

        #                 ],
        #                 rows_num=9,
        #             )
        #             self.table.row_data = values
        #             self.ids.box.add_widget(self.table)

        #         if not not self.table:
        #             self.table.row_data = values
        #     except EmptyClassSpinnerError:
        #         self.empty_spinner_dialog = MDDialog(
        #             title="Warning!",
        #             text="Please select the year and term to proceed",
        #             radius=[40, 7, 40, 7],
        #             auto_dismiss=False,
        #             buttons=[
        #                 MDRectangleFlatButton(
        #                     text="CLOSE", on_release=self.close_empty_spinner_dialog
        #                 ),

        #             ],
        #         )
        #         self.empty_spinner_dialog.open()

    def close_empty_spinner_dialog(self, obj):
        self.empty_spinner_dialog.dismiss()

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class Graphs(Screen):
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_years FROM years")]
    years = values

    def get_income_and_expenditure_graph(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        p_l = c.execute(
            """UPDATE income_and_expenditure SET p_l = income - expenditure""")
        jan = c.execute("""UPDATE income_and_expenditure_previews
                    SET
                    income_preview = SUM(income),
                    expenditure_preview = SUM(expenditure),
                    p_l_preview = SUM(p_l),
                    term_preview = term,
                    year_preview  = year,
                    month_preview = month
                    FROM income_and_expenditure
                    WHERE income_and_expenditure.year =?
                    AND income_and_expenditure.month = 'January'
                    AND income_and_expenditure_previews.month_preview = 'January'""",
                        (self.ids.select_year_spinner.text,))
        feb = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'February'
                AND income_and_expenditure_previews.month_preview = 'February'""",
                        (self.ids.select_year_spinner.text,))
        mar = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'March'
                AND income_and_expenditure_previews.month_preview = 'March'""",
                        (self.ids.select_year_spinner.text,))
        apr = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'April'
                AND income_and_expenditure_previews.month_preview = 'April'""",
                        (self.ids.select_year_spinner.text,))
        may = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'May'
                AND income_and_expenditure_previews.month_preview = 'May'""",
                        (self.ids.select_year_spinner.text,))
        june = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'June'
                AND income_and_expenditure_previews.month_preview = 'June'""",
                         (self.ids.select_year_spinner.text,))
        july = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'July'
                AND income_and_expenditure_previews.month_preview = 'July'""",
                         (self.ids.select_year_spinner.text,))
        august = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'August'
                AND income_and_expenditure_previews.month_preview = 'August'""",
                           (self.ids.select_year_spinner.text,))
        sep = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'September'
                AND income_and_expenditure_previews.month_preview = 'September'""",
                        (self.ids.select_year_spinner.text,))
        october = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'october'
                AND income_and_expenditure_previews.month_preview = 'october'""",
                            (self.ids.select_year_spinner.text,))
        nov = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'November'
                AND income_and_expenditure_previews.month_preview = 'November'""",
                        (self.ids.select_year_spinner.text,))
        dec = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'December'
                AND income_and_expenditure_previews.month_preview = 'December'""",
                        (self.ids.select_year_spinner.text,))
        conn.commit()
        if self.ids.select_data_type_spinner.text == "Bar Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    months = [r[0] for r in c.execute(
                        """SELECT months FROM months""",)]
                    months_position = np.arange(len(months))
                    income = [r[0] for r in c.execute("""SELECT income_preview
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""", (self.ids.select_year_spinner.text,))]
                    expenditure = [r[0] for r in c.execute("""SELECT expenditure_preview
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""", (self.ids.select_year_spinner.text,))]
                    # print(income)
                    # print(expenditure)
                    # print(len(income))
                    if len(income) != 12 and len(expenditure) != 12:
                        raise ValueError
                    plt.xlabel("Months")
                    plt.ylabel("Amount in GHC")
                    plt.bar(months_position-0.2,  income,
                            width=0.4, label="Income")
                    plt.bar(months_position+0.2,  expenditure,
                            width=0.4, label="Expenditure")
                    plt.xticks(months_position, months)
                    plt.style.use("seaborn")
                    plt.legend()
                    plt.tight_layout()
                    plt.title(
                        f"{self.ids.select_year_spinner.text} Academic Calender - Yearly Income & Exenditure Analysis")
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()

            else:
                try:
                    months = [r[0] for r in c.execute(
                        """SELECT months FROM months WHERE months.month_term = ?""", (self.ids.select_term_spinner.text,))]
                    months_position = np.arange(len(months))
                    income = [r[0] for r in c.execute("""SELECT income_preview
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                      (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    expenditure = [r[0] for r in c.execute("""SELECT expenditure_preview
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                           (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    if len(income) != 4 and len(expenditure) != 4:
                        raise ValueError

                    plt.xlabel("Months")
                    plt.ylabel("Amount in GHC")
                    plt.bar(months_position-0.2,  income,
                            width=0.4, label="Income")
                    plt.bar(months_position+0.2,  expenditure,
                            width=0.4, label="Expenditure")
                    plt.xticks(months_position, months)
                    plt.style.use("seaborn")
                    plt.legend()
                    plt.tight_layout()
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Income & Expenditure Analysis - {self.ids.select_year_spinner.text}")
                    plt.show()

                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
        elif self.ids.select_data_type_spinner.text == "Pie Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    p_l = c.execute(
                        """UPDATE income_and_expenditure SET p_l = income - expenditure""")
                    conn.commit()
                    income = [r[0] for r in c.execute("""SELECT SUM(income_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""",
                                                      (self.ids.select_year_spinner.text, ))]
                    expenditure = [r[0] for r in c.execute("""SELECT SUM(expenditure_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""",
                                                           (self.ids.select_year_spinner.text,))]
                    slices = [income, expenditure]
                    labels = ("Income", "Expenditure")
                    explode = (0.02, 0)
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            explode=explode, shadow=True, startangle=270)
                    plt.title(
                        f"{self.ids.select_year_spinner.text} Academic Calender - Yearly Income & Exenditure Analysis")
                    plt.style.use('ggplot')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.legend(loc='upper left')
                    plt.show()
                    print(income)
                    print(expenditure)
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
            else:
                try:
                    # conn = sqlite3.connect("school.db")
                    # c = conn.cursor()
                    # p_l = c.execute(
                    #     """UPDATE income_and_expenditure SET p_l = income - expenditure""")
                    # conn.commit()
                    income = [r[0] for r in c.execute("""SELECT SUM(income_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                      (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    expenditure = [r[0] for r in c.execute("""SELECT SUM(expenditure_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                           (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    # print(income)
                    # print(expenditure)
                    slices = [income, expenditure]
                    labels = ("Income", "Expenditure")
                    explode = (0.02, 0)
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            explode=explode, shadow=True, startangle=270)
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Income & Expenditure Analysis - {self.ids.select_year_spinner.text}")
                    plt.style.use('ggplot')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.legend(loc='upper left')
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Error",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[25, 7, 25, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
        elif self.ids.select_data_type_spinner.text == "Donut Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    # conn = sqlite3.connect("school.db")
                    # c = conn.cursor()
                    # p_l = c.execute(
                    #     """UPDATE income_and_expenditure SET p_l = income - expenditure""")
                    # conn.commit()
                    income = [r[0] for r in c.execute("""SELECT SUM(income_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""",
                                                      (self.ids.select_year_spinner.text,))]
                    expenditure = [r[0] for r in c.execute("""SELECT SUM(expenditure_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""",
                                                           (self.ids.select_year_spinner.text, ))]

                    slices = [income, expenditure]
                    labels = ["Income", "Expenditure"]
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            shadow=True, startangle=270)
                    plt.title(
                        "f{self.ids.select_year_spinner.text} Academic Calender - Yearly Income & Exenditure Analysis")
                    plt.style.use('ggplot')
                    plt.tight_layout()
                    plt.axis('equal')
                    plt.axis('equal')

                    plt.legend(loc='upper left')

                    circle = plt.Circle(
                        xy=[0, 0], radius=.75, facecolor='white')
                    plt.gca().add_artist(circle)
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Error!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[25, 7, 25, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
            else:
                try:
                    # conn = sqlite3.connect("school.db")
                    # c = conn.cursor()
                    # p_l = c.execute(
                    #     """UPDATE income_and_expenditure SET p_l = income - expenditure""")
                    # conn.commit()
                    income = [r[0] for r in c.execute("""SELECT SUM(income_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                      (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    expenditure = [r[0] for r in c.execute("""SELECT SUM(expenditure_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                           (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    slices = [income, expenditure]
                    labels = ["Income", "Expenditure"]
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            shadow=True, startangle=270)
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Income & Expenditure Analysis - {self.ids.select_year_spinner.text}")
                    plt.style.use('ggplot')
                    plt.tight_layout()
                    plt.axis('equal')
                    plt.axis('equal')

                    plt.legend(loc='upper left')

                    circle = plt.Circle(
                        xy=[0, 0], radius=.75, facecolor='white')
                    plt.gca().add_artist(circle)
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Error!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[25, 7, 25, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
        else:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="No Data Exits",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def get_income_graph(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        p_l = c.execute(
            """UPDATE income_and_expenditure SET p_l = income - expenditure""")
        jan = c.execute("""UPDATE income_and_expenditure_previews
                    SET
                    income_preview = SUM(income),
                    expenditure_preview = SUM(expenditure),
                    p_l_preview = SUM(p_l),
                    term_preview = term,
                    year_preview  = year,
                    month_preview = month
                    FROM income_and_expenditure
                    WHERE income_and_expenditure.year =?
                    AND income_and_expenditure.month = 'January'
                    AND income_and_expenditure_previews.month_preview = 'January'""",
                        (self.ids.select_year_spinner.text,))
        feb = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'February'
                AND income_and_expenditure_previews.month_preview = 'February'""",
                        (self.ids.select_year_spinner.text,))
        mar = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'March'
                AND income_and_expenditure_previews.month_preview = 'March'""",
                        (self.ids.select_year_spinner.text,))
        apr = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'April'
                AND income_and_expenditure_previews.month_preview = 'April'""",
                        (self.ids.select_year_spinner.text,))
        may = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'May'
                AND income_and_expenditure_previews.month_preview = 'May'""",
                        (self.ids.select_year_spinner.text,))
        june = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'June'
                AND income_and_expenditure_previews.month_preview = 'June'""",
                         (self.ids.select_year_spinner.text,))
        july = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'July'
                AND income_and_expenditure_previews.month_preview = 'July'""",
                         (self.ids.select_year_spinner.text,))
        august = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'August'
                AND income_and_expenditure_previews.month_preview = 'August'""",
                           (self.ids.select_year_spinner.text,))
        sep = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'September'
                AND income_and_expenditure_previews.month_preview = 'September'""",
                        (self.ids.select_year_spinner.text,))
        october = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'october'
                AND income_and_expenditure_previews.month_preview = 'october'""",
                            (self.ids.select_year_spinner.text,))
        nov = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'November'
                AND income_and_expenditure_previews.month_preview = 'November'""",
                        (self.ids.select_year_spinner.text,))
        dec = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'December'
                AND income_and_expenditure_previews.month_preview = 'December'""",
                        (self.ids.select_year_spinner.text,))
        conn.commit()
        if self.ids.select_data_type_spinner.text == "Bar Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    months = [r[0] for r in c.execute(
                        """SELECT months FROM months""")]
                    months_position = np.arange(len(months))

                    income = [r[0] for r in c.execute("""SELECT income_preview
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""", (self.ids.select_year_spinner.text,))]
                    if len(income) != 12:
                        raise ValueError
                    plt.xlabel("Months")
                    plt.ylabel("Amount in GHC")
                    plt.bar(months_position, income, width=0.4, label="Income")
                    plt.xticks(months_position, months)
                    plt.style.use("seaborn")
                    plt.tight_layout()
                    plt.title(
                        f"{self.ids.select_year_spinner.text} Academic Calender - Yearly Income Analysis")
                    plt.show()
                    print(income)
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()

            else:
                try:
                    months = [r[0] for r in c.execute(
                        """SELECT months FROM months WHERE months.month_term = ?""", (self.ids.select_term_spinner.text,))]
                    months_position = np.arange(len(months))
                    income = [r[0] for r in c.execute("""SELECT income_preview
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                      (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    if len(income) != 4:
                        raise ValueError
                    plt.xlabel("Months")
                    plt.ylabel("Amount in GHC")
                    plt.bar(months_position, income, width=0.4, label="Income")
                    plt.xticks(months_position, months)
                    plt.style.use("seaborn")
                    plt.tight_layout()
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Income Analysis - {self.ids.select_year_spinner.text}")
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()

        elif self.ids.select_data_type_spinner.text == "Pie Chart" or self.ids.select_data_type_spinner.text == "Donut Chart":
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="No Income data exist for Pie charts and Donut Charts",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        else:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="No Data Exits",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def get_expenditure_graph(self):
        if self.ids.select_data_type_spinner.text == "Pie Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    p_l = c.execute(
                        """UPDATE income_and_expenditure SET p_l = income - expenditure""")
                    conn.commit()

                    academic = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Academic'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    canteen = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Canteen'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    tax = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Tax'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    salary = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Salary'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    utility = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Utility'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    miscellaneous = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Miscellaneous'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    if academic == [None] or canteen == [None] or tax == [None] or salary == [None] or utility == [None] or miscellaneous == [None]:
                        raise ValueError
                    explode = (0, 0, 0, 0.02, 0, 0)
                    slices = [academic, canteen, tax,
                              salary, utility, miscellaneous, ]
                    labels = ['Academic', 'Canteen', "Tax",
                              'Salary', "Utility", "Miscellaneous"]
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            explode=explode, startangle=90)
                    plt.title(
                        f"{self.ids.select_year_spinner.text} Academic Calender - Yearly Exenditure Analysis")
                    plt.style.use('ggplot')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.legend(loc='upper left')
                    plt.show()
                    print(slices)
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
            else:
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    academic = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Academic'
                                AND expenditure.year = ?
                                AND expenditure.term = ?
                                """, (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    canteen = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Canteen'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    tax = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Tax'
                                AND expenditure.year = ?
                                AND expenditure.term = ?
                                """, (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    salary = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Salary'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    utility = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Utility'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    miscellaneous = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Miscellaneous'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    if academic == [None]:
                        academic = [0]
                    elif canteen == [None]:
                        canteen = [0]
                    elif tax == [None]:
                        tax = [0]
                    elif salary == [None]:
                        salary = [0]
                    elif utility == [None]:
                        utility = [0]
                    elif miscellaneous == [None]:
                        miscellaneous = [0]

                    explode = (0, 0, 0, 0.02, 0, 0)
                    labels = ['Academic', 'Canteen', "Tax",
                              'Salary', "Utility", "Miscellaneous"]
                    slices = [academic, canteen, tax,
                              salary, utility, miscellaneous]
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            explode=explode, startangle=90)
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Expenditure Analysis - {self.ids.select_year_spinner.text}")
                    plt.style.use('ggplot')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.legend(loc='upper left')
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Notice!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
        elif self.ids.select_data_type_spinner.text == "Donut Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    p_l = c.execute(
                        """UPDATE income_and_expenditure SET p_l = income - expenditure""")
                    conn.commit()

                    academic = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Academic'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    canteen = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Canteen'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    tax = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Tax'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    salary = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Salary'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    utility = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Utility'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    miscellaneous = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Miscellaneous'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    if academic == [None] or canteen == [None] or tax == [None] or salary == [None] or utility == [None] or miscellaneous == [None]:
                        raise ValueError
                    slices = [academic, canteen, tax,
                              salary, utility, miscellaneous, ]
                    labels = ['Academic', 'Canteen', "Tax",
                              'Salary', "Utility", "Miscellaneous"]
                    plt.pie(slices, labels=labels,
                            autopct='%.1f%%', shadow=True, startangle=90)
                    plt.title(
                        "{self.ids.select_year_spinner.text} Academic Calender - Yearly Exenditure Analysis")
                    plt.style.use('ggplot')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.legend(loc='upper left')
                    circle = plt.Circle(
                        xy=[0, 0], radius=.75, facecolor='white')
                    plt.gca().add_artist(circle)
                    plt.show()
                    print(slices)
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Data for the selected timeline may not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
            else:
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    academic = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Academic'
                                AND expenditure.year = ?
                                AND expenditure.term = ?
                                """, (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    canteen = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Canteen'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    tax = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Tax'
                                AND expenditure.year = ?
                                AND expenditure.term = ?
                                """, (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    salary = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Salary'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    utility = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Utility'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    miscellaneous = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Miscellaneous'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    if academic == [None]:
                        academic = [0]
                    elif canteen == [None]:
                        canteen = [0]
                    elif tax == [None]:
                        tax = [0]
                    elif salary == [None]:
                        salary = [0]
                    elif utility == [None]:
                        utility = [0]
                    elif miscellaneous == [None]:
                        miscellaneous = [0]
                    explode = (0, 0, 0, 0.02, 0, 0)
                    labels = ['Academic', 'Canteen', "Tax",
                              'Salary', "Utility", "Miscellaneous"]
                    slices = [academic, canteen, tax,
                              salary, utility, miscellaneous]
                    plt.pie(slices, labels=labels,
                            autopct='%.2f%%', shadow=True, startangle=90)
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Expenditure Analysis - {self.ids.select_year_spinner.text}")
                    plt.style.use('ggplot')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.legend(loc='upper left')
                    circle = plt.Circle(
                        xy=[0, 0], radius=.75, facecolor='white')
                    plt.gca().add_artist(circle)
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Error",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()

                    labels = ["Income", "Expenditure"]
                    colors = ["green", "red"]
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            colors=colors, shadow=True, startangle=90)
                    plt.title("Yearly Exenditure Analysis")
                    plt.style.use('ggplot')
                    plt.tight_layout()
                    plt.axis('equal')
                    plt.axis('equal')

                    plt.legend(loc='upper left')

                    circle = plt.Circle(
                        xy=[0, 0], radius=.75, facecolor='white')
                    plt.gca().add_artist(circle)
                    plt.show()

        elif self.ids.select_data_type_spinner.text == "Bar Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    academic = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Academic'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    canteen = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Canteen'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    tax = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Tax'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    salary = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Salary'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    utility = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Utility'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    miscellaneous = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Miscellaneous'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Academic'""", academic)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Canteen'""", canteen)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Tax'""", tax)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Salary'""", salary)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Utility'""", utility)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Miscellaneous'""", miscellaneous)

                    conn.commit()
                    the_bar = [r[0] for r in c.execute(
                        """SELECT  expense_amt FROM expenditure_barchart""")]

                    expenditure_type = ['Academic', 'Canteen', 'Tax',
                                        'Salary', 'Utility', 'Miscellaneous']
                    xposition = np.arange(len(expenditure_type))

                    plt.xlabel("Expenditure Breakdown")
                    plt.ylabel("Amount in GHC")
                    plt.bar(xposition, the_bar, width=0.4)
                    plt.xticks(xposition, expenditure_type)
                    plt.style.use("seaborn")
                    plt.tight_layout()
                    plt.title(
                        f"{self.ids.select_year_spinner.text} Academic Calender - Yearly Expenditure Analysis")
                    plt.show()

                except (ValueError, TypeError):
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()

            else:
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    academic = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Academic'
                                AND expenditure.year = ?
                                AND expenditure.term = ? """,
                                                        (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text))]
                    canteen = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Canteen'
                                AND expenditure.year = ?
                                AND expenditure.term = ? """,
                                                       (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text))]
                    tax = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Tax'
                                AND expenditure.year = ?
                                AND expenditure.term = ? """,
                                                   (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text))]
                    salary = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Salary'
                                AND expenditure.year = ?
                                AND expenditure.term = ? """,
                                                      (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text))]
                    utility = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Utility'
                                AND expenditure.year = ?
                                AND expenditure.term = ? """,
                                                       (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text))]
                    miscellaneous = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Miscellaneous'
                                AND expenditure.year = ?
                                AND expenditure.term = ? """,
                                                             (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text))]
                    if academic == [None]:
                        academic = [0]
                    elif canteen == [None]:
                        canteen = [0]
                    elif tax == [None]:
                        tax = [0]
                    elif salary == [None]:
                        salary = [0]
                    elif utility == [None]:
                        utility = [0]
                    elif miscellaneous == [None]:
                        miscellaneous = [0]
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Academic'""", academic)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Canteen'""", canteen)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Tax'""", tax)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Salary'""", salary)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Utility'""", utility)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Miscellaneous'""", miscellaneous)

                    conn.commit()
                    the_bar = [r[0] for r in c.execute(
                        """SELECT  expense_amt FROM expenditure_barchart""")]

                    expenditure_type = ['Academic', 'Canteen', 'Tax',
                                        'Salary', 'Utility', 'Miscellaneous']
                    xposition = np.arange(len(expenditure_type))

                    plt.xlabel("Expenditure Breakdown")
                    plt.ylabel("Amount in GHC")
                    plt.bar(xposition, the_bar, width=0.4)
                    plt.xticks(xposition, expenditure_type)
                    plt.style.use("seaborn")
                    plt.tight_layout()
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Expenditure Analysis - {self.ids.select_year_spinner.text}")
                    plt.show()

                except (ValueError, TypeError):
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
        else:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="No Data Exits",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def del_spinner_choices(self):
        self.ids.select_year_spinner.text = "Select Year"
        self.ids.select_year_spinner.background_color = .7, 0, 0, .9

        self.ids.select_term_spinner.text = "Select Term"
        self.ids.select_term_spinner.background_color = .7, 0, 0, .9

        self.ids.select_data_type_spinner.text = "Select Graph Type"
        self.ids.select_data_type_spinner.background_color = .7, 0, 0, .9

    def close_empty_class_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class IncomeExpenditureAnalytics(Screen):
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_years FROM years")]
    years = values

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"


class WindowManager(ScreenManager):
    pass


class SmartTrackerApp(MDApp):
    def build(self):
        theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file("main.kv")


if __name__ == "__main__":
    SmartTrackerApp().run()
