import kivy
import sqlite3
import datetime
import src.exceptions as exceptions
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable


class Fees(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            radius=[40, 7, 40, 7],
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
                raise exceptions.EmptyClassSpinnerError
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
        except exceptions.EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="Please select a class to continue",
                radius=[40, 7, 40, 7],
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
            radius=[40, 7, 40, 7],
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
                raise exceptions.EmptyClassSpinnerError
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
        except exceptions.EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="Please select a class to continue",
                radius=[40, 7, 40, 7],
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
            radius=[40, 7, 40, 7],
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
                raise exceptions.EmptyClassSpinnerError
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
        except exceptions.EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="Please select a class to continue",
                radius=[40, 7, 40, 7],
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
            radius=[40, 7, 40, 7],
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
            radius=[40, 7, 40, 7],
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
    # grade_spinner = Spinner()
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
            radius=[40, 7, 40, 7],
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
                raise exceptions.EmptyClassSpinnerError
            elif self.ids.students_full_name_spinner.text == "Select Name":
                raise exceptions.EmptyClassSpinnerError
            if self.ids.select_payee_spinner.text == "Select Payee":
                raise exceptions.EmptyFieldError
            elif self.ids.payment_type_spinner.text == "Transaction Mode":
                raise exceptions.EmptyFieldError
            elif self.ids.amt.text == '' or int(self.ids.amt.text) <= 0:
                raise exceptions.NoAmountError
            elif self.ids.name_of_payee.text == '':
                raise exceptions.AuthorizationError
            elif self.ids.receipt_no.text == '':
                raise exceptions.AuthorizationError

        except exceptions.EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="No option as been selected for either class or name of student",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        except exceptions.EmptyFieldError:
            self.empty_class_dialog = MDDialog(
                title="Important!",
                text="Select payee type and transaction mode to transact",
                auto_dismiss=False,
                radius=[40, 7, 40, 7],
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        except exceptions.NoAmountError:
            self.empty_class_dialog = MDDialog(
                title="Bad Transaction Alert!",
                text="Amount cannot be less than or equal to 0",
                auto_dismiss=False,
                radius=[40, 7, 40, 7],
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        except exceptions.AuthorizationError:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="Please provide name of payee and receipt number to transact",
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
            conn.commit()
            self.empty_class_dialog = MDDialog(
                title="Success!",
                text=f"You have succesfully made a transaction",
                radius=[40, 7, 40, 7],
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
            radius=[40, 7, 40, 7],
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
    # grade_spinner = Spinner()
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
                raise exceptions.EmptyClassSpinnerError
            if self.ids.students_full_name_spinner.text == "Select name":
                raise exceptions.EmptyClassSpinnerError
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
        except exceptions.EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="Please select a class to continue",
                radius=[40, 7, 40, 7],
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
            radius=[40, 7, 40, 7],
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
